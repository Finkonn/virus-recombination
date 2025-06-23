import pandas as pd

file_path = "BDP_csv/main_SAT2_bdp.csv"
df = pd.read_csv(file_path)

df.columns = [col.strip() for col in df.columns]
df = df.rename(columns={
    'Position in JF749864/Unknown/Unknown/2003/SAT2': 'Position',
    'Recombination breakpoint number (200nt win)': 'RecombinationEvents'
}) 

df_filtered = df[df['RecombinationEvents'] >= 4].copy()

df_filtered['Gap'] = df_filtered['Position'].diff().fillna(0)

df_filtered['Group'] = (df_filtered['Gap'] > 200).cumsum()

regions = df_filtered.groupby('Group')['Position'].agg(['min', 'max']).reset_index()

regions['Length'] = regions['max'] - regions['min']
top2_regions = regions.sort_values(by='Length', ascending=False)

print(top2_regions)

top2_regions.to_csv('SAT2_recomb_free.csv', index=False)
