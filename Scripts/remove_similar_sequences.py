import pandas as pd
from Bio import SeqIO
import argparse
import os

def process_distance_table(distance_table_file, threshold):
    df = pd.read_csv(distance_table_file)
    main_list = list(df['Species 1'].unique())
    check_set = set()

    for element in main_list:
        if element in check_set:
            continue

        filtered_rows = df[df['Species 1'] == element]
        for _, row in filtered_rows.iterrows():
            if row['Dist'] < threshold:
                if row['Species 2'] in main_list:
                    check_set.add(row['Species 2'])

    return check_set

def write_ids_to_file(ids, output_file):
    with open(output_file, "w") as fp:
        for i in ids:
            fp.write(i + '\n')

def remove_sequences(fasta_file, ids_to_remove, output_file):
    filtered_records = []
    for record in SeqIO.parse(fasta_file, 'fasta'):
        if record.id not in ids_to_remove:
            filtered_records.append(record)

    with open(output_file, 'w') as out_file:
        SeqIO.write(filtered_records, out_file, 'fasta')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process distance table and remove sequences from FASTA file.")
    parser.add_argument('-t', '--distance_table', required=True, help="Path to the distance table CSV file.")
    parser.add_argument('-i', '--input_fasta', required=True, help="Path to the input FASTA file.")
    parser.add_argument('-o', '--output_fasta', help="Path to the output FASTA file.")
    parser.add_argument('--threshold', type=float, default=0.03, help="Threshold for distance to remove sequences (default: 0.03).")

    args = parser.parse_args()

    if not args.output_fasta:
        args.output_fasta = os.path.split(args.input_fasta)[0]

    sequences_to_remove = process_distance_table(args.distance_table, args.threshold)
    remove_sequences(args.input_fasta, sequences_to_remove, args.output_fasta)

    print(f"Removed {len(sequences_to_remove)} sequences from the FASTA file.")