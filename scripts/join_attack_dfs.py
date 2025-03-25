import pandas as pd
import os

try:
    # path for files by attack activity
    dataset_path = "data/Attack_Data_Master"

    # list of subdirectories (each representing an attack type)
    attack_dirs = [
        os.path.join(dataset_path, d)
        for d in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, d))
    ]

    # list of all txt files with their corresponding attack type
    files = [
        (
            os.path.join(attack_dir, f),
            "_".join(os.path.basename(attack_dir).split("_")[:-1]),
        )
        for attack_dir in attack_dirs
        for f in os.listdir(attack_dir)
        if f.endswith(".txt")
    ]

# verify if the directory contains files
except FileNotFoundError:
    print("No files found in the dataset path")
    exit()
else:
    print(f"Found {len(files)} attack files")

    # global counter of syscalls per attack type
    syscalls_data = []
    total_syscalls = 0

    # read and process each file
    for file_path, attack_type in files:
        with open(file_path, "r") as f:
            line = f.readline().strip()  # remove spaces
            converted_to_numbers = map(int, line.split())  # convert to integers type
            syscall_list = list(converted_to_numbers)  # save to list
            total_syscalls += len(syscall_list)

            # store syscall_id and attack_type
            for syscall in syscall_list:
                syscalls_data.append((syscall, attack_type))

# create a dataframe with the results
df = pd.DataFrame(syscalls_data, columns=["syscall_id", "attack_type"])

# count frequency of syscalls per attack type
df = df.groupby(["attack_type", "syscall_id"]).size().reset_index(name="frequency")
df = df.sort_values(
    by=["attack_type", "frequency"], ascending=[True, False]
).reset_index(drop=True)

# check if the sum of frequencies matches the total syscalls read
sum_frequencies = df["frequency"].sum()

print(f"Total syscalls read: {total_syscalls}")
print(f"Sum of frequencies: {sum_frequencies}")

if total_syscalls == sum_frequencies:
    print("All its alright")
else:
    print("It's have a problem")
    exit()

# print first rows of the dataframe
print(df.head())

# save the dataframe to a csv file
try:
    df.to_csv("processed_data/attack_dataset.csv", index=False)
    print("\nSaved successfully")
except Exception as e:
    print(f"Error saving the file: {e}")
