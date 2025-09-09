import pandas as pd

metadata = pd.read_excel("metadata.xlsx")  

with open("Maps/genotyped_lineages.txt", "r") as f:
    lines = f.read().splitlines()

lineage_dict = {}
for line in lines:
    parts = line.split("_")
    accession = parts[0]
    lineage = parts[-1]
    if not lineage.endswith("SOUTH"):
        lineage_dict[accession] = lineage

metadata['Lineage'] = metadata['Genbank accession'].map(lineage_dict)

metadata.to_excel("metadata_with_lineage.xlsx", index=False)
