import pandas as pd
from Bio import SeqIO

fastas = SeqIO.parse('Sequences/genotyped.fasta', 'fasta')
fasta_accessions = set()

for fasta in fastas:
    fasta_accessions.add(fasta.id.split('/')[0])

df = pd.read_excel('Tables/classification.xlsx')

df['Match'] = df['Accession no.'].apply(lambda x: 'Yes' if x in fasta_accessions else 'No')

df.to_excel('Tables/classification.xlsx', index=False)

accessions = set()
for num, value in enumerate(df['Match']):
    if value == 'Yes':
        accessions.add(df['Accession no.'].iloc[num])

new_color = "#FF0000"  #Red

with open('Trees/not_colored_nexus_VP1.nexus', 'r') as file:
    nexus_lines = file.readlines()

with open('Trees/VP1_topotype_colored.nexus', 'w') as output_file:
    for line in nexus_lines:
        if line.strip().startswith(tuple(accessions)):
            start = line.find("[&!color=")
            if start != -1:
                end = line.find("]", start)
                if end != -1:
                    line = line[:start + 9] + new_color + line[end:]
        output_file.write(line)