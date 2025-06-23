from Bio import SeqIO
import pandas as pd

def map_ungapped_to_gapped(reference_seq):
    """Creates a mapping from ungapped to gapped coordinates (0-based)"""
    mapping = []
    for i, char in enumerate(reference_seq):
        if char != '-':
            mapping.append(i)
    return mapping

def get_outside_regions(region_df, ungapped_length, split_point):
    """Identifies outside regions and splits at a given split_point (ungapped)"""
    outside_regions = []
    prev_end = 0
    for _, row in region_df.iterrows():
        start = int(row['min']) - 1  # Convert to 0-based
        end = int(row['max']) - 1
        if start > prev_end:
            outside_regions.append((prev_end, start - 1))
        prev_end = end + 1
    if prev_end < ungapped_length:
        outside_regions.append((prev_end, ungapped_length - 1))

    # Now split any region that includes the split_point
    split_regions = []
    for start, end in outside_regions:
        if start <= split_point - 1 <= end:  # split_point is 1-based
            split_regions.append((start, split_point - 2))
            split_regions.append((split_point - 1, end))
        else:
            split_regions.append((start, end))

    return split_regions

def extract_all_regions(records, mapping, outside_regions):
    """Extracts regions from all records and saves to FASTA files"""
    for i, (start, end) in enumerate(outside_regions, 1):
        try:
            gapped_start = mapping[start]
            gapped_end = mapping[end]
        except IndexError:
            continue  # Skip if index is out of bounds

        trimmed_records = []
        for record in records:
            subseq = record.seq[gapped_start:gapped_end+1]
            new_record = record[:0]  # Copy metadata
            new_record.seq = subseq
            new_record.id = record.id
            new_record.description = ""
            trimmed_records.append(new_record)

        with open(f"SAT3_{start+1}-{end+1}.fasta", "w") as output_handle:
            SeqIO.write(trimmed_records, output_handle, "fasta")

def main():
    fasta_file = "MainSerotypes/SAT3.fasta"
    coords_file = "no_similar_recomb_free_coords.csv"
    split_coord = 4276  # 1-based ungapped coordinate to split at

    # Load sequences
    records = list(SeqIO.parse(fasta_file, "fasta"))
    reference_seq = str(records[0].seq)
    mapping = map_ungapped_to_gapped(reference_seq)

    # Load and process regions
    region_df = pd.read_csv(coords_file)
    region_df = region_df.sort_values(by='min')
    outside_regions = get_outside_regions(region_df, len(mapping), split_coord)

    # Extract and save regions
    extract_all_regions(records, mapping, outside_regions)

if __name__ == "__main__":
    main()
