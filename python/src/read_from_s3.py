import json
import time

import polars as pl


def main():
    source = "s3://rust-s3/data.parquet"

    start_time = time.time()

    # df = pl.read_parquet(source)
    df = pl.scan_parquet(source).select(["timestamp", "B1", "E1"]).lazy().collect()
    print(df)

    end_time = time.time()
    print(f"Total Execution Time:{end_time - start_time} seconds")


if __name__ == "__main__":
    main()
