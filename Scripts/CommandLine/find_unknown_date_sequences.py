import argparse
from Bio import SeqIO

def find_unknown_date_sequences(fasta_file, output_file):
    unknown_date_sequences = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        header_parts = record.id.split('/')
        if header_parts[-2] == "Unknown":
            unknown_date_sequences.append(record.id)
    print(f"Количество последовательностей с неизвестной датой: {len(unknown_date_sequences)}")

    if len(unknown_date_sequences) > 0:
        print("Список последовательностей с неизвестной датой:")
        for seq_id in unknown_date_sequences:
            print(seq_id)

        with open(output_file, "w") as output_file_handle:
            for seq_id in unknown_date_sequences:
                output_file_handle.write(seq_id + "\n")
        print(f"Список сохранён в файл: {output_file}")
    else:
        print("Нет последовательностей с неизвестной датой.")

def main():
    parser = argparse.ArgumentParser(description='Find sequences with an unknown date in a FASTA file.')
    parser.add_argument('-f', '--fasta', required=True, help='Input FASTA file containing sequences.')
    parser.add_argument('-o', '--output', required=True, help='Output TXT file to save sequences with unknown dates.')

    args = parser.parse_args()

    find_unknown_date_sequences(args.fasta, args.output)

if __name__ == '__main__':
    main()
