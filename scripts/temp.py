import pandas as pd
import os

dataset_path = "data/Training_Data_Master"
files = [f for f in os.listdir(dataset_path) if f.endswith(".txt")]

df_list = []

for file in files:
    file_path = os.path.join(dataset_path, file)
    df = pd.read_csv(
        file_path, sep=r"\s+", header=None, engine="python"
    )  # Usa raw string
    df_list.append(df)

df_combined = pd.concat(df_list, ignore_index=True)

print(df_combined.head())  # Verifica las primeras filas
print(df_combined.shape)  # Revisa la estructura del DataFrame
