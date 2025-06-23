import argparse
from Bio import SeqIO

def read_annotations(file_path):
    """Read the annotations file into a dictionary."""
    annotations = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('/')
                accession = parts[0]
                annotations[accession] = line
    return annotations

def update_and_filter_fasta(fasta_path, annotations, output_path):
    """Update headers in FASTA file and remove sequences with unknown dates."""
    with open(output_path, 'w') as output_file:
        for record in SeqIO.parse(fasta_path, "fasta"):
            accession = record.id.split('/')[0]
            if accession in annotations:
                # Update header
                new_header = annotations[accession]
                record.description = new_header
                record.id = new_header
            
            # Check if the updated (or original) header has an unknown date
            if "Unknown" not in record.description.split('/')[-2]:
                SeqIO.write(record, output_file, "fasta")

def main():
    parser = argparse.ArgumentParser(description="Update FASTA headers based on annotation file and filter out sequences with unknown dates.")
    parser.add_argument('-a', "--annotations", required=True, help="Path to the annotations file")
    parser.add_argument('-f', "--fasta", required=True, help="Path to the input FASTA file")
    parser.add_argument('-o', "--output", required=True, help="Path to the output FASTA file")
    
    args = parser.parse_args()
    
    # Read the annotations file
    annotations = read_annotations(args.annotations)
    
    # Update FASTA headers and filter out sequences with unknown dates
    update_and_filter_fasta(args.fasta, annotations, args.output)
    
    print("Headers successfully updated and sequences with unknown dates have been removed.")

if __name__ == "__main__":
    main()
