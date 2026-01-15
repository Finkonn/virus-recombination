import os
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

excel_path = "meta_no_probang_removed_seqs.xlsx"
accession_df = pd.read_excel(excel_path)
accessions_to_remove = set(accession_df["Genbank accession"].astype(str).str.strip())

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".fasta"):
            fasta_path = os.path.join(root, file)
            new_name = file.replace(".fasta", "_no_probang.fasta")
            new_path = os.path.join(root, new_name)
            
            sequences_to_keep = []
            for record in SeqIO.parse(fasta_path, "fasta"):
                genbank_accession = record.id.split("/")[0]
                if genbank_accession not in accessions_to_remove:
                    sequences_to_keep.append(record)
            os.remove(fasta_path)
            
            SeqIO.write(sequences_to_keep, new_path, "fasta")
print('Done')