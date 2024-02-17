import json

import pyarrow.parquet as pq

# Path to your Parquet file
parquet_file_path = "output_with_metadata.parquet"

# Reading the Parquet file
parquet_file = pq.ParquetFile(parquet_file_path)

# Accessing the schema
schema = parquet_file.schema_arrow

# Extracting the custom metadata from the schema
custom_metadata = schema.metadata

# Assuming you stored your custom metadata under the key 'custom_metadata'
if b"custom_metadata" in custom_metadata:
    custom_metadata_json = custom_metadata[b"custom_metadata"].decode("utf-8")
    custom_metadata_dict = json.loads(custom_metadata_json)
    print("Custom Metadata:", custom_metadata_dict)
else:
    print("No custom metadata found.")
