# Analysis of natural recombination of Foot-and-mouth disease virus

The purpose of the work is to analyze natural recombination in the foot-and-mouth disease virus (FMDV, genus Aphthovirus), test the hypothesis that there is reproductive isolation between groups of FMDV serotypes, and analyze the temporal dynamics of recombination.

## Analyzing .gb records and extracting useful information

Extract fasta file with coding sequences, and modify a header to contain valuable information: **>GenbankAC/country/host/year/serotype**.

## Align extracted sequences

Using script **trans_alignment.py** to translate the sequences from RNA to proteins and from proteins back to RNA, using **MAFFT v7.520**

### Usage
```
trans_alignment.py -input INPUT_FILE 
```

## Extract and Process Protein Coordinates from GenBank and FASTA Files

This script extracts mature peptide (mat_peptide) coordinates from a GenBank file, maps these coordinates to a reference sequence from a FASTA file, and accounts for gaps in the reference sequence. It outputs two CSV files: one with the original protein coordinates and another with the gapped coordinates.

### Usage
```
-g, --genbank: Path to the input GenBank file containing mat_peptide features. (Required)
-f, --fasta: Path to the input FASTA file containing the reference sequence. (Required)
-p, --protein_output: Path to save the output CSV file with protein coordinates. (Required)
-o, --gapped_output: Path to save the output CSV file with gapped protein coordinates. (Required)
```
```bash
python get_protein_coords.py -g <genbank_file> -f <fasta_file> -p <protein_output_file> -o <gapped_output_file>
```

## Genotyping

Using script **genotyping.py** to map colors from .nexus tree to certain serotypes (shown in **color_serotype.csv**). Change 'Unknown' serotypes to new ones and check for conflicts (**genotyping_result.txt**). Save new serotypes into **qualifiers_table_filtered.csv**

### Usage 
```
genotyping.py [-h] -in_rep INPUT_REP_FASTA -in_tree INPUT_FILE_TREE
                     -in_csv INPUT_FILE_CSV
```

## Ambiguous Segment Length Plotter

This script plots the distribution of the longest ambiguous segment lengths in sequences from a given FASTA file. The script reads a FASTA file, identifies segments with ambiguous nucleotide characters (R, Y, S, W, K, M, B, D, H, V, N), and plots a histogram showing the distribution of the lengths of these ambiguous segments.

### Usage
```
max_ambiguous_length.py [-h] -input INPUT
```

## Remove similar sequences

Script **remove_similar_sequences.py** uses the **distance_table.csv** obtained from MEGA, to remove all sequences that are similar in an alignment up to a certain threshold. 

### Usage 
```
-t, --distance_table: Path to the distance table CSV file. (Required)
-i, --input_fasta: Path to the input FASTA file. (Required)
-o, --output_fasta: Path to the output FASTA file. (Optional)
--threshold: Threshold for distance to remove sequences. Default is 0.03. (Optional)
```
```
remove_similar_sequences.py -t ../distance_table.csv -i ../Sequences/filtered_alignment_no_ambiguous_fewer_gaps.fasta
```

## Match Accessions Between FASTA and Excel Files

This script checks for matching accession numbers between sequences in a FASTA file and an Excel file, then updates the Excel file to indicate whether each accession number was found in the FASTA file.

### Usage
```
-f, --fasta: Path to the input FASTA file containing sequences. (Required)
-e, --excel: Path to the input Excel file with accession numbers. (Required)
-o, --output: Path to save the output Excel file with the 'Match' column added. If not provided, the input Excel file will be overwritten. (Optional)
```
```bash
python match_topotypes.py -f <fasta_file> -e <excel_file> [-o <output_file>]
```

## Color Nexus File Based on Accessions from an Excel File

This script updates a Nexus file by applying a specified color to lines corresponding to accessions marked as "Yes" in an Excel file.

### Usage
```
-e, --excel: Path to the input Excel file containing accession numbers and their "Match" status. (Required)
-n, --nexus_input: Path to the input Nexus file that needs to be colored. (Required)
-o, --nexus_output: Path to save the output Nexus file with the updated colors. (Required)
-c, --color: Color code to apply to matching accessions. Default is #FF0000 (red). (Optional)
```
```bash
python color_topotypes.py -e <excel_file> -n <nexus_input_file> -o <nexus_output_file> [-c <color_code>]
```

## Find Sequences with Unknown Dates in a FASTA File

This script identifies sequences in a FASTA file that have "Unknown" as the date and outputs the list of such sequences to a text file.

### Usage
```
-f, --fasta: Path to the input FASTA file containing sequences. (Required)
-o, --output: Path to the output text file where the list of sequences with unknown dates will be saved. (Required)
```
```bash
python find_unknown_date_sequences.py -f <fasta_file> -o <output_file>
```

## Split a FASTA File by Serotype

This script splits a FASTA file into separate files based on the serotype information found in each sequence header. Each serotype will be saved as a separate FASTA file in the specified output directory.

### Usage
```
-i, --input_fasta: Path to the input FASTA file containing sequences. (Required)
-o, --output_dir: Path to the output directory where the serotype-specific FASTA files will be saved. (Required)
```
```bash
python split_fasta_by_serotype.py -i <input_fasta> -o <output_dir>
```

## Fetch Sequences from NCBI Using Accession Numbers

This script fetches nucleotide sequences from NCBI based on accession numbers listed in an Excel file and saves them to a FASTA file.

### Usage
```
-f, --file: Path to the Excel file containing accession numbers. (Required) 
-e, --email: Your email address (required by NCBI to use the Entrez service). (Required)
-o, --output: Path to the output FASTA file where the sequences will be saved. (Required)
```
```bash
python get_topotype_sequences.py -f <excel_file> -e <your_email> -o <output_fasta>
```

## Map Serotypes to Sequences in a FASTA File

This script maps serotypes from a CSV table to sequences in a FASTA file. It updates the sequence IDs in the FASTA file with the corresponding serotype information and saves the result to a new FASTA file.

### Usage
```
-f, --fasta_file: Path to the input FASTA file containing sequences. (Required)
-t, --table_file: Path to the CSV table file containing GenBank accessions and corresponding serotypes. (Required)
-o, --output_fasta: Path to the output FASTA file where the updated sequences will be saved. (Required)
```
```bash
python map_serotype.py -f <input_fasta> -t <table_file> -o <output_fasta>
```