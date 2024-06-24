from Bio import AlignIO
from Bio.Align import AlignInfo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

alignment = AlignIO.read("filtered_alignment_no_ambiguous_less_gaps.fasta", "fasta")

summary_align = AlignInfo.SummaryInfo(alignment)
consensus = summary_align.dumb_consensus()

# Calculate the similarity of each sequence to the consensus
similarities = []
for record in alignment:
    seq = record.seq
    similarity = sum(c1 == c2 for c1, c2 in zip(seq, consensus)) / len(consensus)
    similarities.append((record.id, similarity))

# Create a DataFrame to hold the results
df = pd.DataFrame(similarities, columns=["Sequence_ID", "Similarity"])
df.to_csv('sequence_similarities.csv', index=False)

# Calculate statistical summaries
mean_similarity = df["Similarity"].mean()
median_similarity = df["Similarity"].median()
min_similarity = df["Similarity"].min()
max_similarity = df["Similarity"].max()

# Print statistical summaries
print(f"Mean Similarity: {mean_similarity:.2f}")
print(f"Median Similarity: {median_similarity:.2f}")
print(f"Min Similarity: {min_similarity:.2f}")
print(f"Max Similarity: {max_similarity:.2f}")

bins = np.arange(0, 1.1, 0.1)
df['Similarity_Group'] = pd.cut(df['Similarity'], bins, include_lowest=True)
grouped = df['Similarity_Group'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
grouped.plot(kind='bar')
plt.xlabel("Similarity Group")
plt.ylabel("Number of Sequences")
plt.title("Distribution of Sequence Similarities to Consensus")
plt.xticks(rotation=45)
plt.show()