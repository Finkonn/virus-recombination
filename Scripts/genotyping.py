import argparse
import re
import csv
import os
from Bio import SeqIO

def genotyping(rep_in, tree_in, csv_in):
    '''
    The function assigns genotype/serotype/taxon to sequences in alignments in fasta format using colored tree in nexus format.
    Output is file in fasta format with updated sequence names.
    rep_in - repository of fasta alignments
    tree_in - colored phylogenetic tree in nexus format
    csv_in - comma separated table with colors and corresponding genogroups/serotype/taxon
        Example:
        #3333ff,GI
        #00ccff,GII
    
    '''
    tl_fl = 0  # taxlabels have began
    names_dict = {}  # names_dict[seq_name] = serotype
    unknown_counter = 0
    conflict_counter = 0

    def csv_reader(csv_file_input, input_str):
        '''
        Reads csv-file and outputs the short name of a variable.

        Input:
            csv_file_input - string - name of csv-file in the directory of the script
            input_str - string - a string value

        Output:
            output_str - string - short designation from csv-file
        '''

        with open(csv_file_input) as csv_file:
            output_str = ''
            reader = csv.DictReader(csv_file, delimiter=",",
                                    fieldnames=["base", "new"])
            for line in reader:
                base = re.compile(line["base"])
                if base.match(input_str):
                    output_str = line["new"].strip()
            return output_str
    # parse tree file and find lines with taxa name and hex color
    with open(tree_in, "r") as tree_f:
        for line in tree_f:
            if re.match('\ttaxlabels', line):
                tl_fl = 1
                continue
            if tl_fl == 1:
                if line == ';\n':
                    tl_fl = 0
                else:
                    # search hex code of color
                    color = re.search(r'#[0-9a-z]+', line)
                    if color:
                        color = color.group()
                        # taxa name
                        seq_name = re.search(r"[A-Za-z0-9_\-\/.]+", line).group()
                        #seq_name = seq_name[:6].replace('_', '-') + seq_name[6:]
                        seq_name = seq_name.split('_')[0]
                        # seq_name - taxon
                        names_dict[seq_name] = csv_reader(csv_in, color)

    files = os.listdir(rep_in)
    for fasta_f in files:
        if fasta_f.split('_')[-1:] == ['genotyped.fasta']:
            continue
        fasta_f = rep_in + fasta_f
        fasta_out = '.'.join(fasta_f.split('.')[:-1]) + '_genotyped.fasta'
        fasta_seq = SeqIO.parse(fasta_f, 'fasta')
        record_list = []
        for record in fasta_seq:           
            seq_name = record.id.split('/')[0]

            if seq_name in names_dict.keys():
                if record.id.endswith('Unknown'):              
                    record.id = record.id[:-7] + names_dict[seq_name]
                    unknown_counter += 1
                else: 
                    if record.id.split('/')[-1] != names_dict[seq_name] and record.id.split('/')[-1] == 'CATHAY':
                            record.id = record.id[:-7] + '-' + 'CATHAY'
                    elif record.id.split('/')[-1] != names_dict[seq_name] and record.id.split('/')[-1] == 'Pan-Asia-O':
                            pass
                    elif record.id.split('/')[-1] != names_dict[seq_name]:
                        print('Serotype conflict: ', record.id)
                        print('Old serotype: ', record.id.split('/')[-1])
                        print('New serotype: ', names_dict[seq_name])
                        record.id = record.id[:-len(record.id.split('/')[-1])] + names_dict[seq_name]
                        conflict_counter +=1
                record.description = ''
            record_list.append(record)
        SeqIO.write(record_list, fasta_out, 'fasta')
        #fasta_seq.close()
    print('Unknown serotypes fixed: ', unknown_counter)
    print('Serotype conflicts: ', conflict_counter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_rep", "--input_rep_fasta", type=str,
                        help="Input repository with files in fasta format. \
                        Alignment will not be processed if its name ends with \"_genotyped.fasta\"", required=True)
    parser.add_argument("-in_tree", "--input_file_tree", type=str,
                        help="Input colored tree in nexus format", required=True)
    parser.add_argument("-in_csv", "--input_file_csv", type=str,
                        help="Input table in csv format with colors in hex format and genotypes",
                        required=True)
    args = parser.parse_args()
    genotyping(args.input_rep_fasta, args.input_file_tree, args.input_file_csv)
