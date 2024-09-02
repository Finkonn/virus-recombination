import argparse
import pandas as pd
from Bio import SeqIO

def map_serotype(fasta_file, table_file, output_fasta):
    # Load the CSV table
    df = pd.read_csv(table_file)  
    
    # Parse the input FASTA file
    fasta = SeqIO.parse(fasta_file, 'fasta')
    updated_records = []
    
    for record in fasta:
        seq_name = record.id.split('/')[0]  # Extract the sequence name
        
        # Check if the sequence name exists in the DataFrame
        if seq_name in df['GenBankAccession'].values:
            serotype = df.loc[df['GenBankAccession'] == seq_name, 'Genotyped serotype'].values[0]
            
            # Update the sequence ID and description with the serotype
            id_parts = record.id.split('/')
            id_parts[-1] = serotype
            record.id = '/'.join(id_parts)
            record.description = record.id  
        
        updated_records.append(record)
        
    # Save the updated records to the output FASTA file
    with open(output_fasta, 'w') as output_handle:
        SeqIO.write(updated_records, output_handle, 'fasta')
    
    print(f"Updated FASTA file saved as: {output_fasta}")

def main():
    parser = argparse.ArgumentParser(description='Map serotypes from a CSV table to sequences in a FASTA file.')
    parser.add_argument('-f', '--fasta_file', required=True, help='Input FASTA file with sequences.')
    parser.add_argument('-t', '--table_file', required=True, help='CSV table file containing GenBank accessions and serotypes.')
    parser.add_argument('-o', '--output_fasta', required=True, help='Output FASTA file to save sequences with updated serotypes.')

    args = parser.parse_args()

    map_serotype(args.fasta_file, args.table_file, args.output_fasta)

if __name__ == '__main__':
    main()
