import pandas as pd
import ast
import argparse
from Bio import SeqIO

def extract_sequences(input_fasta, input_table, product):
    # Load the coordinates from the CSV file
    gapped_coords = pd.read_csv(input_table)
    
    # Find the coordinates for the specified product
    product_coords = gapped_coords.loc[gapped_coords['Product'] == product, 'Gapped_Coordinates'].values[0]
    product_coords = ast.literal_eval(product_coords)
    
    output_fasta = f"{product}.fasta"
    
    start_coordinate = product_coords[0]
    end_coordinate = product_coords[1]

    # Open input and output FASTA files
    with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
        # Parse input FASTA file
        for record in SeqIO.parse(infile, "fasta"):
            # Extract sequence based on coordinates
            extracted_seq = record.seq[start_coordinate-1:end_coordinate]  # Adjust for 0-based indexing

            # Write the extracted sequence to the output file with the original header
            outfile.write(f">{record.id}\n")
            outfile.write(f"{extracted_seq}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract sequences from a FASTA file based on coordinates from a CSV file for a specified product.')
    parser.add_argument('-i', '--input_fasta', required=True, help='Path to the input FASTA file')
    parser.add_argument('-t', '--input_table', required=True, help='Path to the CSV file containing the coordinates')
    parser.add_argument('-p', '--product', required=True, help='Product name to extract sequences for')
    
    args = parser.parse_args()
    
    extract_sequences(args.input_fasta, args.input_table, args.product)