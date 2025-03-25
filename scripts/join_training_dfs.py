import pandas as pd
import os
from collections import Counter

try:
    # path for files by normal activity
    dataset_path = "data/Training_Data_Master"

    # list of files
    files = [
        os.path.join(dataset_path, f)
        for f in os.listdir(dataset_path)
        if f.endswith(".txt")
    ]

# verify if the contain files
except FileNotFoundError:
    print("No files found in the dataset path")
    exit()
else:
    print(f"Found {len(files)} files")

    # global counter of syscalls
    syscalls_counter = Counter()
    total_syscalls = 0

    # read and process each file
    for file in files:

        with open(file, "r") as f:
            line = f.readline().strip()  # remove spaces
            converted_to_numbers = map(int, line.split())  # convert to integers type
            syscall_list = list(converted_to_numbers)  # save to list
            total_syscalls += len(syscall_list)
            syscalls_counter.update(syscall_list)

# create a dataframe with the results
df = pd.DataFrame(syscalls_counter.items(), columns=["syscall_id", "frequency"])
df = df.sort_values(by="frequency", ascending=False).reset_index(drop=True)

# check if the sum of frequencies match with the total datasets read
sum_frequencies = df["frequency"].sum()

print(f"Total syscalls read: {total_syscalls}")
print(f"Sum of frequencies: {sum_frequencies}")

if total_syscalls == sum_frequencies:
    print("All its alright")
else:
    print("It's have a problem")
    exit()

# print fist rows of the dataframe
print(df.head())

# save the dataframe to a csv file
try:
    df.to_csv("processed_data/training_dataset.csv", index=False)
    print("\nSaved successfully")
except Exception as e:
    print(f"error saving the file: {e}")
