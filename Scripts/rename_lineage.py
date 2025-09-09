import pandas as pd
import re

classification_df = pd.read_excel('../Tables/classification.xlsx')

# Преобразуем таблицу в словарь: accession → {Serotype, Lineage}
classification_dict = classification_df.set_index('Accession no.').T.to_dict()

def rename_sequence(seq_name):
    accession = seq_name.split('_')[0]
    length = len(seq_name.split('_'))
    
    if accession in classification_dict and length < 5:
        serotype = classification_dict[accession]['Serotype'].replace(' ', '')
        lineage = str(classification_dict[accession]['Lineage']) \
            .replace('(', '').replace(')', '').replace(',', '').replace(' ', '-')
        
        return f"{accession}_{serotype}_{lineage}"
    return seq_name

# Чтение файла дерева
with open('../Trees/VP1/VP1_with_topotypes.treefile', 'r') as file:
    tree_data = file.read()

# Находим все имена таксонов (Accession_что-то)
sequences = re.findall(r'\b[A-Z0-9]+_[A-Za-z0-9_]+\b', tree_data)

# Переименовываем
renamed_sequences = {seq: rename_sequence(seq) for seq in sequences}

for old_name, new_name in renamed_sequences.items():
    tree_data = tree_data.replace(old_name, new_name)

# Сохраняем в новый Nexus
with open('../Trees/VP1_with_lineages_renamed.nexus', 'w') as file:
    file.write(tree_data)

print("Renaming completed with lineage!")
