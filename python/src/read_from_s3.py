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


"""
Collator will save the data as csv and put into S3 as asset_data.csv
SDC will save data into current location as postcode_dumps.parquet

Metrics will get entire csv from S3
Metrics will get only the rows and columns in needs from the parquet file
Metrics will go to Dynamo to get the propeties of the asset

Will do what it has to do on the dataframe it has
Will then upload the dataframe to S3 as a parquet file as asset_metrics.parquet
"""
