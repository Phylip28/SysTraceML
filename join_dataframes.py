import pandas as pd
import os

# path for files by normal activity
dataset_path = "data/Training_Data_Master"

# list of files
files = [f for f in os.listdir(dataset_path) if f.endswith(".txt")]

# list of dataframes
dfs = []

# read all archives and append to dfs
for file in files:
    full_path = os.path.join(dataset_path, file)

    # read file before to process
    with open(full_path, "r") as f:
        sample = f.readline().strip()
        print(f"File: {file} -> {sample}")  # show the content

    # read the file as dataframe
    df = pd.read_csv(full_path, sep=r"\s+", header=None, names=["syscall_id"])
    dfs.append(df)

# join all dataframes
df_combined = pd.concat(dfs, ignore_index=True)

# show first lines
print(df_combined.head())

# save the dataframe
df_combined.to_csv("data/Training_Data_Master/joined_data.csv", index=False)
