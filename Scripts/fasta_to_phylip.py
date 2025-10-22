import os
from Bio import SeqIO

input_root = "RecombFreeSequences"
output_root = "PhylipSequences"

os.makedirs(output_root, exist_ok=True)

for dirpath, _, filenames in os.walk(input_root):
    for filename in filenames:
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            input_path = os.path.join(dirpath, filename)

            relative_path = os.path.relpath(dirpath, input_root)
            output_dir = os.path.join(output_root, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_filename = os.path.splitext(filename)[0] + ".phylip"
            output_path = os.path.join(output_dir, output_filename)

            records = list(SeqIO.parse(input_path, "fasta"))
            if records: 
                count = SeqIO.write(records, output_path, "phylip-relaxed")
                print(f"Converted {count} records from {input_path} to {output_path}")
            else:
                print(f"Skipped empty file: {input_path}")
