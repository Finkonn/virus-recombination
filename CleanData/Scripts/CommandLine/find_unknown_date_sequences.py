import argparse
from Bio import SeqIO

def find_unknown_date_sequences(fasta_file, output_file):
    unknown_date_sequences = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        header_parts = record.id.split('/')
        if header_parts[-2] == "Unknown":
            unknown_date_sequences.append(record.id)
    print(f"Number of unknown dates: {len(unknown_date_sequences)}")

    if len(unknown_date_sequences) > 0:
        print("List of sequences without dates:")
        for seq_id in unknown_date_sequences:
            print(seq_id)

        with open(output_file, "w") as output_file_handle:
            for seq_id in unknown_date_sequences:
                output_file_handle.write(seq_id + "\n")
        print(f"List saved to file: {output_file}")
    else:
        print("No sequences with unknown dates")

def main():
    parser = argparse.ArgumentParser(description='Find sequences with an unknown date in a FASTA file.')
    parser.add_argument('-f', '--fasta', required=True, help='Input FASTA file containing sequences.')
    parser.add_argument('-o', '--output', required=True, help='Output TXT file to save sequences with unknown dates.')

    args = parser.parse_args()

    find_unknown_date_sequences(args.fasta, args.output)

if __name__ == '__main__':
    main()
