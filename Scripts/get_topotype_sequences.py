from Bio import Entrez, SeqIO
import pandas as pd
import time

file_path = 'classification.xlsx'
df = pd.read_excel(file_path)

accession_list = df['Accession no.'].dropna().tolist()

Entrez.email = "your_email@example.com"

with open("Sequences/topotypes.fasta", "w") as fasta_file:
    for accession in accession_list:
        handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
        record = handle.read()
        handle.close()

        fasta_file.write(record)