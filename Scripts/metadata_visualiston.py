import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

metadata = pd.read_csv("Tables/metadata.csv")

metadata['serotype'] = metadata['serotype'].str.strip()
metadata['Topotype'] = metadata['Topotype'].str.strip()

serotypes = metadata['serotype'].value_counts().reset_index()
serotypes.columns = ['Category', 'Count']
serotypes['Group'] = 'Serotype'

metadata['Topotype'] = metadata['Topotype'].replace({
    'EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH': 'EURO-SA',
    'MIDDLE-EAST-SOUTH-ASIA-ME-SA': 'ME-SA',
    'III-NORTHWEST-ZIMBABWE-NWZ': 'NWZ-III',
    'I-NORTHWEST-ZIMBABWE-NWZ': 'NWZ-I',
    'I-SOUTHEAST-ZIMBABWE-SEZ': 'SEZ'
})

topotypes = metadata['Topotype'].value_counts().reset_index()
topotypes.columns = ['Category', 'Count']
topotypes = topotypes[topotypes['Count'] >= 10]
topotypes['Group'] = 'Topotype'

grouped = pd.concat([serotypes, topotypes], ignore_index=True)


serotype_data = grouped[grouped['Group'] == 'Serotype'].sort_values('Count', ascending=False)
topotype_data = grouped[grouped['Group'] == 'Topotype'].sort_values('Count', ascending=False)

data_by_group = {
    'Серотип': serotype_data,
    'Топотип': topotype_data
}

fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=False)

for ax, (group_name, data) in zip(axes, data_by_group.items()):
    sns.barplot(
        data=data,
        x='Count',
        y='Category',
        ax=ax,
        palette='Paired'
    )
    ax.set_title(group_name, fontsize=28)
    ax.set_xlabel('Количество', fontsize=24)
    ax.set_ylabel('', fontsize=24)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    max_count = data['Count'].max()
    
    if group_name == 'Серотип':
        ax.set_xlim(0, max_count * 1.2)
    else:
        ax.set_xlim(0, max_count * 1.1)

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', fontsize=20, padding=4)


plt.tight_layout()
plt.show()
