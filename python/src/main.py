import time

# import pandas as pd
import polars as pl


def main():
    start_time = time.time()
    # Pandas
    # df = pd.read_csv("test.csv")
    # df["Subscription Date"] = pd.to_datetime(df["Subscription Date"])
    # df_small = df[df["Subscription Date"] > "2021-01-01"]
    # df_agg = df_small.groupby("Country").size().reset_index(name="counts")
    # df_sort = df_agg.sort_values(by="counts")
    # print(df_sort)

    # Polars Eager Execution
    df = pl.read_csv("test.csv")
    df_small = df.filter(pl.col("Subscription Date") > "2021-01-01")
    df_agg = df_small.group_by("Country").agg([pl.len().alias("count")])
    df_sort = df_agg.sort(by="count")
    print(df_sort)

    # Polars Lazy Execution
    # q = (
    #     pl.scan_csv("test.csv")
    #     .filter(pl.col("Subscription Date") > "2021-01-01")
    #     .group_by("Country")
    #     .agg([pl.len().alias("count")])
    #     .sort(by="count")
    # )
    # df = q.collect()
    # print(df)

    end_time = time.time()
    print(f"Total Execution Time:{end_time - start_time} seconds")


if __name__ == "__main__":
    main()
