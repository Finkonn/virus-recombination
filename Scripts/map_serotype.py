import pandas as pd
from Bio import SeqIO

def map_serotype(fasta_file, table_file, output_fasta):
    # Step 1: Read the table file into a DataFrame
    df = pd.read_csv(table_file)  # Adjust sep parameter based on your file's delimiter
    
    # Step 2: Parse the FASTA file
    fasta = SeqIO.parse(fasta_file, 'fasta')
    updated_records = []
    
    # Step 3: Iterate over each record in the FASTA file
    for record in fasta:
        # Extract the sequence name
        seq_name = record.id.split('/')[0]
        
        # Check if the sequence name is in the DataFrame
        if seq_name in df['GenBankAccession'].values:
            # Get the corresponding 'Genotypedserotype' value
            serotype = df.loc[df['GenBankAccession'] == seq_name, 'Genotyped serotype'].values[0]
            
            # Step 4: Update the last element of record.id
            id_parts = record.id.split('/')
            id_parts[-1] = serotype
            record.id = '/'.join(id_parts)
            record.description = record.id  # Update description to match the new id
        
        # Collect the updated record
        updated_records.append(record)
    
    # Write the updated records to a new FASTA file
    with open(output_fasta, 'w') as output_handle:
        SeqIO.write(updated_records, output_handle, 'fasta')

map_serotype('../Sequences/no_similar.fasta', '../qualifiers_table_filtered.csv','../Sequences/genotyped.fasta')