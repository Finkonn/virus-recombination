import pandas as pd

input_file = "metadata.csv" 
output_folder = "output/"   

df = pd.read_csv(input_file)

import os
os.makedirs(output_folder, exist_ok=True)

for serotype, group in df.groupby('serotype'):
    output_file = os.path.join(output_folder, f"{serotype}.csv")
    group.to_csv(output_file, index=False)

print(f"Files have been saved to the '{output_folder}' folder.")
