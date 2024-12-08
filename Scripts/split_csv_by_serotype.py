import pandas as pd

# Load your CSV file
input_file = "metadata.csv"  # Replace with your file name
output_folder = "output/"    # Specify the output folder

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Ensure the output folder exists
import os
os.makedirs(output_folder, exist_ok=True)

# Group the DataFrame by the 'serotype' column and save each group to a separate file
for serotype, group in df.groupby('serotype'):
    # Define the output file name
    output_file = os.path.join(output_folder, f"{serotype}.csv")
    # Save the group to a CSV file
    group.to_csv(output_file, index=False)

print(f"Files have been saved to the '{output_folder}' folder.")
