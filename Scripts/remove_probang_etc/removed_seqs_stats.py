import pandas as pd

df = pd.read_excel('meta_no_probang_removed_seqs.xlsx')

serotype_counts = df['Serotype'].value_counts()
country_counts = df['Country'].value_counts()
year_counts = df['Year'].value_counts()

print("Serotype distribution:")
print(serotype_counts)
print("\nCountry distribution:")
print(country_counts)
print("\nYear distribution:")
print(year_counts)