import pandas as pd
import re
import matplotlib.colors as mcolors

classification_df = pd.read_excel('Tables/classification.xlsx')

classification_df = classification_df[classification_df['Accession no.'].notna()]

unique_lineages = classification_df['Lineage'].dropna().unique()

def generate_colors(n):
    return [mcolors.to_hex(c) for c in mcolors.hsv_to_rgb([(i/n, 1.0, 1.0) for i in range(n)])]

colors = generate_colors(len(unique_lineages))

lineage_to_color = {
    lineage: colors[i % len(colors)]
    for i, lineage in enumerate(unique_lineages)
}

accession_to_lineage = classification_df.set_index('Accession no.')['Lineage'].to_dict()

def color_sequence(seq_name):
    accession = seq_name.split('_')[0]
    
    if accession in accession_to_lineage:
        lineage = accession_to_lineage[accession]
        color = lineage_to_color.get(lineage, 'black') 
        return f"{seq_name}[&!color={color}]"
    
    return seq_name 

with open('Trees/VP1_with_lineages_renamed.nexus', 'r') as file:
    nexus_data = file.read()

taxa_block_match = re.search(r'begin taxa;.*?taxlabels(.*?);', nexus_data, re.DOTALL)
if taxa_block_match:
    taxa_block = taxa_block_match.group(1)

    taxa_lines = taxa_block.strip().splitlines()

    modified_lines = []
    for i, line in enumerate(taxa_lines):
        line = line.strip()
        if line:  
            colored_sequence = color_sequence(line)  
            if i == 0:
                modified_lines.append(colored_sequence)
            else:
                modified_lines.append(f"\t{colored_sequence}")
        else:
            modified_lines.append(line)

    modified_taxa_block = "\n".join(modified_lines)
    modified_taxa_block = "\n" + modified_taxa_block

    nexus_data = re.sub(r'(begin taxa;.*?taxlabels)(.*?)(;)', f'\\1{modified_taxa_block}\\3', nexus_data, flags=re.DOTALL)

with open('colored_treefile_lineages.nexus', 'w') as file:
    file.write(nexus_data)

print("Lineages colored successfully!")
