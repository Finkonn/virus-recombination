import argparse
import pandas as pd
from Bio import SeqIO

def filter_fasta(csv_file, fasta_file, output_fasta, removed_txt):
    # Load the CSV file and extract the accession numbers to remove
    df = pd.read_csv(csv_file)
    accession_to_remove = set(df['GenBankAccession'].dropna().tolist())

    # Parse the input FASTA file
    records = list(SeqIO.parse(fasta_file, "fasta"))

    filtered_records = []
    removed_records = []

    for record in records:
        accession = record.id.split('.')[0] 
        if accession in accession_to_remove:
            removed_records.append(accession)
        else:
            filtered_records.append(record)

    # Write the filtered records to the output FASTA file
    with open(output_fasta, "w") as output_handle:
        SeqIO.write(filtered_records, output_handle, "fasta")

    num_removed = len(removed_records)
    print(f"Удалено {num_removed} последовательностей.")
    if num_removed > 0:
        print("Список удаленных последовательностей:")
        print(", ".join(removed_records))

    # Write the removed accessions to a text file
    with open(removed_txt, "w") as removed_handle:
        for accession in removed_records:
            removed_handle.write(accession + "\n")

def main():
    parser = argparse.ArgumentParser(description='Filter sequences from a FASTA file based on accessions listed in a CSV file.')
    parser.add_argument('-c', '--csv_file', required=True, help='Path to the CSV file containing GenBank accessions to remove.')
    parser.add_argument('-f', '--fasta_file', required=True, help='Path to the input FASTA file.')
    parser.add_argument('-o', '--output_fasta', required=True, help='Path to the output FASTA file where filtered sequences will be saved.')
    parser.add_argument('-r', '--removed_txt', required=True, help='Path to the text file where removed accessions will be saved.')

    args = parser.parse_args()

    filter_fasta(args.csv_file, args.fasta_file, args.output_fasta, args.removed_txt)

if __name__ == '__main__':
    main()
