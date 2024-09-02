from Bio import SeqIO

fasta_file = "Sequences/genotyped.fasta"

unknown_date_sequences = []

for record in SeqIO.parse(fasta_file, "fasta"):
    header_parts = record.id.split('/')
    if len(header_parts) > 3 and header_parts[-2] == "Unknown":
        unknown_date_sequences.append(record.id)

num_unknown = len(unknown_date_sequences)
print(f"Количество последовательностей с неизвестной датой: {num_unknown}")

if num_unknown > 0:
    print("Список последовательностей с неизвестной датой:")
    for seq_id in unknown_date_sequences:
        print(seq_id)

with open("Txt/unknown_date_sequences.txt", "w") as output_file:
    for seq_id in unknown_date_sequences:
        output_file.write(seq_id + "\n")
