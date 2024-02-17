import json

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Example data
data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}

# Creating a DataFrame from the data
df = pd.DataFrame(data)

# Convert the DataFrame to a PyArrow Table
table = pa.Table.from_pandas(df)

# Define custom metadata
custom_metadata = {
    "key1": "value1",
    "key2": "value2",
}

# Convert the custom metadata to the appropriate format (stringified JSON here)
metadata_str = json.dumps(custom_metadata)

# Add the custom metadata to the schema
schema_with_metadata = table.schema.with_metadata({b"custom_metadata": metadata_str.encode("utf-8")})

# Create a new table with the updated schema, preserving the data
table_with_metadata = pa.Table.from_pandas(df, schema=schema_with_metadata)

# Write the table to a Parquet file with custom metadata
pq.write_table(table_with_metadata, "output_with_metadata.parquet")
