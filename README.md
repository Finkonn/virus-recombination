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

## Excise protein sequence

Get protein coordinates (**protein_coords.csv**) from the reference sequence (**referense_sequence.gb**), and then calculate these coordinates in an alignment (**gapped_protein_coords.csv**) using script **get_protein_coords.ipynb**. Using the gapped coordinates, excise VP1 sequence from the alignment (**VP1.fasta**). Script - **excise_protein.ipynb**.

For comparison, **VP1.fasta** was generated using the script, and based on reference sequence protein coordinates, but **VP1_handmade.fasta** was manually extracted using **AliView**. 

## Genotyping

Using script **genotyping.py** to map colors from .nexus tree to certain serotypes (shown in **color_serotype.csv**). Change 'Unknown' serotypes to new ones and check for conflicts (**genotyping_result.txt**). Save new serotypes into **qualifiers_table_filtered.csv**

### Usage 
```
genotyping.py [-h] -in_rep INPUT_REP_FASTA -in_tree INPUT_FILE_TREE
                     -in_csv INPUT_FILE_CSV
```