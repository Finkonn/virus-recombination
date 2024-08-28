import os
from Bio import SeqIO

def split_fasta_by_serotype(input_fasta, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    serotype_dict = {}

    # Read and parse the FASTA file
    with open(input_fasta, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            header_parts = record.description.split('/')
            serotype = header_parts[-1]
            
            if serotype not in serotype_dict:
                serotype_dict[serotype] = []
                
            serotype_dict[serotype].append(record)

    # Write each serotype to a separate FASTA file in the output directory
    for serotype, records in serotype_dict.items():
        output_file = os.path.join(output_dir, f"{serotype}.fasta")
        with open(output_file, "w") as output_handle:
            SeqIO.write(records, output_handle, "fasta")

input_fasta = "../Sequences/genotyped.fasta"
output_dir = "../Sequences/serotype_fastas_dir"
split_fasta_by_serotype(input_fasta, output_dir)
