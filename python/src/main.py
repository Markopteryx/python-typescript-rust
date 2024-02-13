import datetime as dt
import logging
import re
import time
from typing import Optional

import polars as pl
from pydantic import BaseModel
from pytest import param

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MetricParams(BaseModel):
    has_solar: bool
    solar_system_size: Optional[float]
    solar_system_install_date: Optional[str]


def calculate_metrics(data: pl.DataFrame, params: MetricParams) -> None:
    # Check for solar
    solar = False
    if ("B1" in data.columns or "B3" in data.columns) and params.has_solar:
        solar = True

    data = calculate_demand(data)

    if solar:
        data = calculate_solar(data, params)

    hourly = resample(data)

    with pl.Config(tbl_cols=hourly.width):
        print(hourly)


def calculate_demand(df: pl.DataFrame) -> pl.DataFrame:
    e_columns = [col for col in df.columns if col.startswith("E")]
    if "E1" not in df.columns:
        df = df.with_columns(df.select(e_columns).sum_horizontal().alias("E1"))

    df = df.with_columns(df.select(e_columns).sum_horizontal().alias("E1"))

    b_columns = [col for col in df.columns if col.startswith("B")]
    if "B1" not in df.columns:
        df = df.with_columns(pl.lit(0).alias("B1"))

    df = df.with_columns(df.select(b_columns).sum_horizontal().alias("B1"))

    if "E1" not in df.columns:
        raise ValueError("Input DataFrame must include E1 column.")

    interval = (df["timestamp"][1] - df["timestamp"][0]).seconds / 3600

    df = df.with_columns(
        [
            (pl.col("E1") / interval).alias("Demand Actual"),
            pl.lit(0).alias("Controlled Loads"),
        ]
    )

    # Check for "_CL" columns and sum them if they exist
    if any("_CL" in col for col in df.columns):
        cl_columns = [col for col in df.columns if "_CL" in col]
        df = df.with_columns(df.select(cl_columns).sum_horizontal().alias("Controlled Loads"))

    if "B1" in df.columns:
        df = df.with_columns((pl.col("B1") / interval).alias("Supply Actual"))

    if "K1" in df.columns:
        df = df.with_columns((pl.col("K1") / interval).alias("Demand Reactive"))

        if "Q1" in df.columns:
            df = df.with_columns((pl.col("Q1") / interval).alias("Supply Reactive"))

            df = df.with_columns(
                ((pl.col("Demand Reactive") ** 2 + pl.col("Demand Actual") ** 2) ** 0.5).alias("Demand Apparent")
            )

            # Calculate Power Factor
            df = df.with_columns((pl.col("Demand Actual") / pl.col("Demand Apparent")).alias("Power Factor"))
    return df


def calculate_solar(df: pl.DataFrame, params: MetricParams) -> pl.DataFrame:
    required_columns = ["performance", "Supply Actual", "Demand Actual"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Input DataFrame must include '{col}' column.")

    df = df.with_columns((pl.col("performance") / 100).alias("performance"))

    solar_system_age = 0
    if params.solar_system_install_date is not None:
        install_date = dt.datetime.strptime(params.solar_system_install_date, "%Y-%m-%d").date()
        diff = dt.datetime.now().date() - install_date
        solar_system_age = round(diff.days / 365)

    if params.solar_system_size is None:
        raise ValueError("Solar system size must be provided for solar metrics calculation.")

    df = df.with_columns(
        (pl.col("performance") * params.solar_system_size * (0.99**solar_system_age)).alias("Solar Generated")
    )

    # Calculate 'Solar Generated' as the max of itself and 'Supply Actual'
    df = df.with_columns(
        pl.when(pl.col("Solar Generated") > pl.col("Supply Actual"))
        .then(pl.col("Solar Generated"))
        .otherwise(pl.col("Supply Actual"))
        .alias("Solar Generated")
    )

    # Calculate 'Solar Used', clipping values at 0.0
    df = df.with_columns((pl.col("Solar Generated") - pl.col("Supply Actual")).clip(0.0).alias("Solar Used"))

    # Calculate 'Demand Total'
    df = df.with_columns((pl.col("Solar Used") + pl.col("Demand Actual")).alias("Demand Total"))

    return df


def resample(df: pl.DataFrame) -> pl.DataFrame:
    columns_to_aggregate = [pl.col(col).mean().alias(col) for col in df.columns if col != "timestamp"]
    hourly = (
        df.with_columns(pl.col("timestamp").set_sorted())
        .group_by_dynamic("timestamp", every="1h", closed="left")
        .agg(columns_to_aggregate)
    )

    return hourly


def main():
    start_time = time.time()
    params: MetricParams = MetricParams(has_solar=True, solar_system_size=5.0, solar_system_install_date="2021-01-01")

    df = (
        pl.read_parquet("../../data/data.parquet")
        .drop("interstate_renewables_percentage")
        .with_columns(pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S"))
    )

    calculate_metrics(df, params)

    end_time = time.time()
    print(f"Total Execution Time:{end_time - start_time} seconds")


if __name__ == "__main__":
    main()
