import os
import argparse
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

    print(f"FASTA files have been written to the directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Split a FASTA file by serotype and save each serotype in a separate file.')
    parser.add_argument('-i', '--input_fasta', required=True, help='Input FASTA file with sequences.')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory where serotype-specific FASTA files will be saved.')

    args = parser.parse_args()

    split_fasta_by_serotype(args.input_fasta, args.output_dir)

if __name__ == '__main__':
    main()
