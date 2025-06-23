from Bio import SeqIO
import pandas as pd

def map_ungapped_to_gapped(reference_seq):
    mapping = []
    for i, char in enumerate(reference_seq):
        if char != '-':
            mapping.append(i)
    return mapping

def get_outside_regions(region_df, ungapped_length):
    outside_regions = []
    prev_end = 0
    for _, row in region_df.iterrows():
        start = int(row['min'])
        end = int(row['max'])
        if start > prev_end:
            outside_regions.append((prev_end, start - 1))
        prev_end = end + 1
    if prev_end < ungapped_length:
        outside_regions.append((prev_end, ungapped_length - 1))
    return outside_regions

def extract_all_regions(records, mapping, outside_regions):
    for i, (start, end) in enumerate(outside_regions, 1):
        try:
            gapped_start = mapping[start]
            gapped_end = mapping[end]
        except IndexError:
            continue  

        trimmed_records = []
        for record in records:
            subseq = record.seq[gapped_start:gapped_end+1]
            new_record = record[:0] 
            new_record.seq = subseq
            new_record.id = record.id
            new_record.description = ""
            trimmed_records.append(new_record)

        with open(f"SAT2_{start+1}-{end+1}.fasta", "w") as output_handle:
            SeqIO.write(trimmed_records, output_handle, "fasta")

def main():
    fasta_file = "MainSerotypes/SAT2.fasta"
    coords_file = "SAT2_recomb_free.csv"

    records = list(SeqIO.parse(fasta_file, "fasta"))
    reference_seq = str(records[0].seq)
    mapping = map_ungapped_to_gapped(reference_seq)

    region_df = pd.read_csv(coords_file) 
    region_df = region_df.sort_values(by='min')
    outside_regions = get_outside_regions(region_df, len(mapping))

    extract_all_regions(records, mapping, outside_regions)

if __name__ == "__main__":
    main()