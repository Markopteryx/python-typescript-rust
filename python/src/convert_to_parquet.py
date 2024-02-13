import glob
import os

import pandas as pd

# Path to your folder containing CSV files
folder_path = "data"

# Use glob to find all CSV files
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# List to hold data
dataframes_list = []

# Read each CSV file and append to list
for file in csv_files:
    df = pd.read_csv(file)
    dataframes_list.append(df)

# Concatenate all dataframes
large_df = pd.concat(dataframes_list, ignore_index=True)

# Export to Parquet
large_df.to_parquet("combined_data.parquet")
