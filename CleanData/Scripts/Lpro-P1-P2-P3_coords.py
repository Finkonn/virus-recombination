import pandas as pd
from Bio import SeqIO

def find_gapped_positions(sequence, ungapped_coordinates):
    gapped_coordinates = []
    gapped_index = 0
    for i, letter in enumerate(sequence):
        if letter != "-":
            gapped_index += 1
            if gapped_index in ungapped_coordinates:
                gapped_coordinates.append(i + 1)

    seq = sequence[gapped_coordinates[0] - 1:gapped_coordinates[1]]
    return seq, gapped_coordinates

def get_first_sequence(fasta_file):
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            return str(record.seq)

fasta_file = '..\Sequences\main.fasta'
sequence = get_first_sequence(fasta_file)

products = [['Lpro', 1, 603],['P1', 1050, 2614],['P2', 2806, 4275],['P3', 4276, 6999]]

results = []
for product in products:
    ungapped_coordinates = list(range(product[1], product[2] + 1))
    seq, gapped_coordinates = find_gapped_positions(sequence, ungapped_coordinates)
    results.append({
        'Product': product[0],
        'Gapped_Coordinates': [gapped_coordinates[0], gapped_coordinates[-1]]
    })
results_df = pd.DataFrame(results)
results_df.to_csv('P1-P2-P3_gapped.csv', index=False)
