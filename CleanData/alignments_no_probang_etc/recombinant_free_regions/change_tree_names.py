import argparse
import re
import os
from Bio import SeqIO

def change_tree_names(fasta_name, tree_name):
    with open(tree_name) as tree_file:
        tree_line = tree_file.readline()
    
    original_tree_line = tree_line
    

    seqs = SeqIO.to_dict(SeqIO.parse(fasta_name, 'fasta'))
    seq_names = list(seqs.keys())
    
    changes_made = False
    
    for seq in seq_names:
        seq_ac = seq.split('/')[0]
        print(f"Looking for: {seq_ac}")
        
        search_seq = re.search(seq_ac + r'[\w\n_\.\?\/-]+', tree_line)
        
        if search_seq:
            found_seq = search_seq.group()
            if found_seq == seq:
                print(f"  Already matches: {seq}")
                continue
            else:
                print(f"  Found: {found_seq} -> Replacing with: {seq}")
                tree_line = re.sub(seq_ac + r'[\w\n_\.\?\/-]+', seq, tree_line)
                changes_made = True
        else:
            print(f"  WARNING: '{seq_ac}' not found in tree, skipping...")
            continue
    
    if changes_made:
        tree_file_name_new = os.path.splitext(tree_name)[0] + '_new.treefile'
        print(f"Writing updated tree to: {tree_file_name_new}")
        
        with open(tree_file_name_new, 'w') as tree_file:
            tree_file.write(tree_line)
    else:
        print("No changes were made to the tree file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-in_fasta", "--input_fasta", type=str,
                        help="Input fasta file with updated names", required=True)
    parser.add_argument("-in_tree", "--input_file_tree", type=str,
                        help="Input tree file in nwk format", required=True)
    args = parser.parse_args()
    change_tree_names(args.input_fasta, args.input_file_tree)