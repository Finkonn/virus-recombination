import os
import argparse
import pandas as pd
from Bio import SeqIO

def split_fasta(fasta_file, coords, serotype, output_folder):
    sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    
    for idx, (start, end) in enumerate(coords):
        region_name = f"{serotype}_Coord_{start}_{end}.fasta"
        region_path = os.path.join(output_folder, region_name)
        
        with open(region_path, 'w') as out_fasta:
            for record in sequences.values():
                seq_region = record.seq[start:end]
                SeqIO.write(record[:0] + seq_region, out_fasta, "fasta")

def main():
    parser = argparse.ArgumentParser(description="Split FASTA files based on coordinates from an XLSX file.")
    parser.add_argument("xlsx_file", help="Path to the XLSX file with coordinates.")
    parser.add_argument("serotypes_folder", help="Path to the folder containing FASTA files.")
    parser.add_argument("output_folder", help="Path to save the output split FASTA files.")
    args = parser.parse_args()

    df = pd.read_excel(args.xlsx_file)
    
    current_serotype = None
    coords = []
    
    for idx, row in df.iterrows():
        serotype = row['Serotype']
        
        if pd.notna(serotype):  # New serotype found
            if current_serotype is not None:
                serotype_folder = os.path.join(args.output_folder, current_serotype)
                if not os.path.exists(serotype_folder):
                    os.makedirs(serotype_folder)
                fasta_file = os.path.join(args.serotypes_folder, f"{current_serotype}.fasta")
                split_fasta(fasta_file, coords, current_serotype, serotype_folder)
            
            # Update the current serotype and reset coordinates list
            current_serotype = serotype
            coords = []
        
        # Append the current coordinate pair to the list
        coords.append((row['CoordStart'], row['CoordEnd']))

    # Handle the last serotype
    if current_serotype is not None:
        serotype_folder = os.path.join(args.output_folder, current_serotype)
        if not os.path.exists(serotype_folder):
            os.makedirs(serotype_folder)
        fasta_file = os.path.join(args.serotypes_folder, f"{current_serotype}.fasta")
        split_fasta(fasta_file, coords, current_serotype, serotype_folder)

if __name__ == "__main__":
    main()
