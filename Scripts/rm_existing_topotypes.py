import pandas as pd
from Bio import SeqIO

csv_file = 'qualifiers_table_filtered.csv'
df = pd.read_csv(csv_file)
accession_to_remove = set(df['GenBankAccession'].dropna().tolist())

fasta_file = 'Sequences/topotypes.fasta'
records = list(SeqIO.parse(fasta_file, "fasta"))

filtered_records = []
removed_records = []

for record in records:
    accession = record.id.split('.')[0]  
    if accession in accession_to_remove:
        removed_records.append(accession)
    else:
        filtered_records.append(record)

with open("Sequences/filtered_topotypes.fasta", "w") as output_handle:
    SeqIO.write(filtered_records, output_handle, "fasta")

num_removed = len(removed_records)
print(f"Удалено {num_removed} последовательностей.")
if num_removed > 0:
    print("Список удаленных последовательностей:")
    print(", ".join(removed_records))

with open("Txt/removed_topotypes.txt", "w") as removed_handle:
    for accession in removed_records:
        removed_handle.write(accession + "\n")
