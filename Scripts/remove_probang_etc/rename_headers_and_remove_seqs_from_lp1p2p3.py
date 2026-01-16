import sys
from pathlib import Path
from Bio import SeqIO
import argparse
'''
на вход - референсный фаста файл с хедерами и директория с фаста файлами
на выход - эти фаста файлы без последовательностей в референсе и с обновленными хедерами
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--reference", help="Reference FASTA file")
    parser.add_argument("-d","--input_dir", help="Directory with FASTA files to filter")
    parser.add_argument("-o", "--output_dir", default="filtered", help="Output directory")
    args = parser.parse_args()

    ref_ids = {}
    with open(args.reference) as f:
        for record in SeqIO.parse(f, "fasta"):
            seq_id = record.id.split('/')[0]
            ref_ids[seq_id] = str(record.id)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    input_dir = Path(args.input_dir)
    for fasta_file in input_dir.glob("*.fasta"):
        kept_records = []
        
        with open(fasta_file) as f:
            for record in SeqIO.parse(f, "fasta"):
                seq_id = str(record.id).split('/')[0]
                if seq_id in ref_ids:
                    record.id = ref_ids[seq_id]
                    record.description = ref_ids[seq_id]
                    kept_records.append(record)

        output_file = output_dir / fasta_file.name
        with open(output_file, "w") as f:
            SeqIO.write(kept_records, f, "fasta")

        print(f"{fasta_file.name}: kept {len(kept_records)} sequences", file=sys.stderr)

if __name__ == "__main__":
    main()