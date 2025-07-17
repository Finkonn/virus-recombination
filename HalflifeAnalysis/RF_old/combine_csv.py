import pandas as pd
import os
from glob import glob

folders = ["Asia1_Lpro", "Asia1_P2", "Asia1_P3",
           "O_Lpro", "O_P2", "O_P3",
           "SAT1_Lpro", "SAT1_P2", "SAT1_P3"]

all_data = []

for folder in folders:
    csv_files = glob(os.path.join(folder, "*.csv"))
    
    for file in csv_files:
        df = pd.read_csv(file)
        all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

combined_df.to_csv("combined_data.csv", index=False)
