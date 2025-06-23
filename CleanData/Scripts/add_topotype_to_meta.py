import pandas as pd

with open("../Maps/genotyped_topotypes.txt", "r") as file:
    lines = file.read().strip().split("\n")

metadata = pd.read_csv("../R_gradient_colors/metadata.csv")

metadata['GBAC_ID'] = metadata['GBAC'].apply(lambda x: x.split('/')[0])

def process_line(line):
    parts = line.split('_')
    gbac_id = parts[0]
    topotype = parts[-1]
    return gbac_id, topotype

processed_data = []

for line in lines:
    gbac_id, topotype = process_line(line)
    if gbac_id in metadata['GBAC_ID'].values:
        processed_data.append((gbac_id, topotype))

topotype_df = pd.DataFrame(processed_data, columns=['GBAC_ID', 'Topotype'])

result = metadata.merge(topotype_df, on='GBAC_ID', how='left')

result = result.drop(columns=['GBAC_ID'])

result.to_csv("updated_metadata.csv", index=False)

print("Файл успешно обработан и сохранен как 'updated_metadata.csv'.")
