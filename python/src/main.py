import datetime as dt
import logging
import re
import time
from typing import Optional

import polars as pl
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MetricParams(BaseModel):
    has_solar: bool
    solar_system_size: Optional[float]
    solar_system_install_date: Optional[str]


def calculate_metrics(data: pl.DataFrame, params: MetricParams) -> None:
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
    E_columns = [col for col in df.columns if col.startswith("E")]
    if "E1" not in df.columns:
        df = df.with_columns(df.select(E_columns).sum_horizontal().alias("E1"))

    df = df.with_columns(df.select(E_columns).sum_horizontal().alias("E1"))

    B_columns = [col for col in df.columns if col.startswith("B")]
    if "B1" not in df.columns:
        df = df.with_columns(pl.lit(0).alias("B1"))

    df = df.with_columns(df.select(B_columns).sum_horizontal().alias("B1"))

    if "E1" not in df.columns:
        raise ValueError("Input DataFrame must include E1 column.")

    df = df.with_columns((df["timestamp"].diff().shift(-1).cast(pl.Int64) / 3_600_000_000).alias("Interval"))

    # Handle potential NaN values
    df = df.with_columns(
        pl.when(df["Interval"].is_null()).then(pl.lit(None)).otherwise(df["Interval"]).alias("Interval")
    )

    df = df.with_columns([(pl.col("E1") / pl.col("Interval")).alias("Grid Usage"), pl.lit(0).alias("CL Usage")])

    # Check for "_CL" columns and sum them if they exist
    if any("_CL" in col for col in df.columns):
        CL_columns = [col for col in df.columns if "_CL" in col]
        df = df.with_columns(df.select(CL_columns).sum_horizontal().alias("CL Usage"))

    if "B1" in df.columns:
        df = df.with_columns((pl.col("B1") / pl.col("Interval")).alias("Solar Actual"))

    if "K1" in df.columns:
        df = df.with_columns((pl.col("K1") / pl.col("Interval")).alias("Reactive Demand"))

        if "Q1" in df.columns:
            df = df.with_columns((pl.col("Q1") / pl.col("Interval")).alias("Reactive Solar"))

            df = df.with_columns(
                ((pl.col("Reactive Demand") ** 2 + pl.col("Grid Usage") ** 2) ** 0.5).alias("Apparent Demand")
            )

            # Calculate Power Factor
            df = df.with_columns((pl.col("Grid Usage") / pl.col("Apparent Demand")).alias("Power Factor"))

    return df.drop(["Interval"])


def calculate_solar(df: pl.DataFrame, params: MetricParams) -> pl.DataFrame:
    required_columns = ["performance", "Solar Actual", "Grid Usage"]
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
        pl.when(pl.col("Solar Generated") > pl.col("Solar Actual"))
        .then(pl.col("Solar Generated"))
        .otherwise(pl.col("Solar Actual"))
        .alias("Solar Generated")
    )

    # Calculate 'Solar Used', clipping values at 0.0
    df = df.with_columns((pl.col("Solar Generated") - pl.col("Solar Actual")).clip(0.0).alias("Solar Used"))

    df = df.with_columns((pl.col("Solar Used") + pl.col("Grid Usage")).alias("Total Usage"))

    # Here we impute the missing "Total Usage" values (indicative of sensor failures when zero) by calculating
    # the mean of the adjacent (above and below) "Total Usage" values. It specifically targets cases where the
    # sensor failure is implied by a zero "Total Usage" and a negative difference between "Solar Generated" and
    # "Solar Actual", suggesting an erroneous reading rather than actual zero usage.
    mean_imputation = (df["Total Usage"].shift(-1).fill_null(0) + df["Total Usage"].shift(1).fill_null(0)) / 2
    mask = (df["Total Usage"] == 0) & (df["Solar Generated"] - df["Solar Actual"] < 0)
    df = df.with_columns(pl.when(mask).then(mean_imputation).otherwise(df["Total Usage"]).alias("Total Usage"))
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
    params: MetricParams = MetricParams(has_solar=True, solar_system_size=5000, solar_system_install_date="2016-01-07")

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
