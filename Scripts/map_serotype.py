import pandas as pd
from Bio import SeqIO

def map_serotype(fasta_file, table_file, output_fasta):
    df = pd.read_csv(table_file)  
    
    fasta = SeqIO.parse(fasta_file, 'fasta')
    updated_records = []
    
    for record in fasta:
        seq_name = record.id.split('/')[0]
        
        if seq_name in df['GenBankAccession'].values:
            serotype = df.loc[df['GenBankAccession'] == seq_name, 'Genotyped serotype'].values[0]
            
            id_parts = record.id.split('/')
            id_parts[-1] = serotype
            record.id = '/'.join(id_parts)
            record.description = record.id  
        
        updated_records.append(record)
        
    # Save file
    with open(output_fasta, 'w') as output_handle:
        SeqIO.write(updated_records, output_handle, 'fasta')

map_serotype('Sequences/filtered_alignment_no_ambiguous_fewer_gaps.fasta', 'qualifiers_table_filtered.csv','Sequences/genotyped.fasta')