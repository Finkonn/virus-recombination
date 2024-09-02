import argparse
import pandas as pd
from Bio import SeqIO

def match_accessions(fasta_file, excel_file, output_file=None):
    # Parse the FASTA file and extract accession numbers
    fastas = SeqIO.parse(fasta_file, 'fasta')
    fasta_accessions = set()

    for fasta in fastas:
        fasta_accessions.add(fasta.id.split('/')[0])

    # Load the Excel file
    df = pd.read_excel(excel_file)

    # Add a 'Match' column based on whether the accession is in the FASTA set
    df['Match'] = df['Accession no.'].apply(lambda x: 'Yes' if x in fasta_accessions else 'No')

    # Write the updated DataFrame back to an Excel file
    output_path = output_file if output_file else excel_file
    df.to_excel(output_path, index=False)
    print(f"Updated Excel file saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Check for matching accessions between a FASTA file and an Excel file.')
    parser.add_argument('-f', '--fasta', required=True, help='Input FASTA file containing sequences.')
    parser.add_argument('-e', '--excel', required=True, help='Input Excel file with accession numbers.')
    parser.add_argument('-o', '--output', help='Output Excel file to save results. If not provided, the input Excel file will be overwritten.')

    args = parser.parse_args()

    match_accessions(args.fasta, args.excel, args.output)

if __name__ == '__main__':
    main()
