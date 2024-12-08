import argparse
from Bio import SeqIO

def load_accession_list(accession_file):
    #Load accession numbers from the file into a set.
    with open(accession_file, 'r') as f:
        accessions = {line.strip() for line in f}
    return accessions

def filter_fasta(fasta_file, output_file, accessions_to_remove):
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        accession = record.id.split('/')[0]
        if accession not in accessions_to_remove:
            sequences.append(record)

    SeqIO.write(sequences, output_file, "fasta")

def main():
    parser = argparse.ArgumentParser(description="Filter out sequences from a FASTA file based on an accession list.")
    parser.add_argument('-a', "--accession_file", help="Path to the file containing accession numbers to remove.")
    parser.add_argument('-f', "--fasta_file", help="Path to the input FASTA file.")
    parser.add_argument('-o', "--output_file", help="Path to the output FASTA file where filtered sequences will be saved.")
    
    args = parser.parse_args()
    
    # Load the accession list
    accessions_to_remove = load_accession_list(args.accession_file)

    # Filter the FASTA file
    filter_fasta(args.fasta_file, args.output_file, accessions_to_remove)

    print(f"Filtered sequences have been written to {args.output_file}")

if __name__ == "__main__":
    main()
