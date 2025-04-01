import argparse
import hashlib
import re
import sys
import os
import csv
import dendropy as dpy
import numpy as np

locval_re = re.compile(r'[0-9]+\.[0-9E\-]+')

def parse_beast_tree_node_info(tree):
    for nd in tree.postorder_node_iter():
        node_comment = nd._get_annotations()
        for annot in node_comment:
            if str(annot).startswith('posterior='):
                posterior = float(locval_re.search(str(annot)).group())
                nd.posterior = posterior
            if str(annot).startswith('height='):
                height = float(locval_re.search(str(annot)).group())
                nd.height = height
    return tree

def sort_bipart(bipart_str):
    if '((' in bipart_str:
        bipart_l = bipart_str.split('), (')
        for i in range(len(bipart_l)):
            bipart_l[i] = bipart_l[i].strip('((').strip('));')
            if len(bipart_l[i]) > 1:
                part_l = bipart_l[i].split(', ')
                part_l.sort()
                bipart_l[i] = ','.join(part_l)
        bipart_l.sort()
        return f"(({bipart_l[0]}),({bipart_l[1]}))"
    return ""

def add_hashes(tree, timescaled=False):
    tree_hashes = {}
    subtree_heights = {} if timescaled else None
    for nd in tree.postorder_node_iter():
        if nd.is_leaf():
            continue
        subtree = dpy.Tree(seed_node=nd.extract_subtree())
        subtree.encode_bipartitions()
        bipart_list = [sort_bipart(bip.split_as_newick_string(subtree.taxon_namespace)) for bip in subtree.encode_bipartitions()]
        bipart_list.sort()
        stri_bipart = ';'.join(bipart_list[1:])
        h = hashlib.new('sha256', usedforsecurity=False)
        h.update(stri_bipart.encode('utf-8'))
        nd.hash = h.hexdigest()
        tree_hashes[nd.hash] = re.sub(r"\)[0-9]+", ")", nd._as_newick_string(edge_lengths=None))
        if timescaled:
            min_leaf_height = min(leaf.height for leaf in nd.leaf_iter())
            subtree_heights[nd.hash] = min_leaf_height
    return (tree_hashes, subtree_heights) if timescaled else tree_hashes

def get_common_subtrees(tree1, subtree_times1, hashes_tree2, posterior_thr=None):
    heights, common_subtrees = [], []
    stack = [tree1.seed_node]
    while stack:
        node = stack.pop()
        if node.is_leaf():
            continue
        if node.hash in hashes_tree2:
            if posterior_thr is None or node.posterior > posterior_thr:
                heights.append(node.height - subtree_times1[node.hash])
                common_subtrees.append(hashes_tree2[node.hash])
            else:
                stack.extend(node._child_nodes)
        else:
            stack.extend(node._child_nodes)
    return heights, common_subtrees

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tree1", "--tree_beast", type=str, required=True, help="BEAST дерево (nexus)")
    parser.add_argument("-tree2", "--tree2", type=str, required=True, help="Сравниваемое дерево (newick/nexus)")
    parser.add_argument("-pthr", "--posterior_threshold", type=float, help="Порог для posterior значений")
    parser.add_argument("-serotype", "--serotype", type=str, required=True, help="Серотип (A, O, C и т.д.)")
    parser.add_argument("-region", "--region", type=str, required=True, help="Регион (Lpro, P1 и т.д.)")
    parser.add_argument("-output", "--output", type=str, required=True, help="Файл для сохранения результатов")
    
    args = parser.parse_args()
    serotype, region = args.serotype, args.region
    print(f"\n=== Обработка серотипа: {serotype}, региона: {region} ===\n")
    
    tree1 = dpy.Tree.get_from_path(args.tree_beast, 'nexus')
    tree1 = parse_beast_tree_node_info(tree1)
    
    try:
        tree2 = dpy.Tree.get_from_path(args.tree2, 'nexus')
    except:
        try:
            tree2 = dpy.Tree.get_from_path(args.tree2, 'newick')
        except:
            print("Ошибка: не удалось прочитать tree2!")
            sys.exit(1)
    
    hashes_tree1, subtree_times1 = add_hashes(tree1, timescaled=True)
    hashes_tree2 = add_hashes(tree2)
    
    heights, subtrees = get_common_subtrees(tree1, subtree_times1, hashes_tree2, args.posterior_threshold)
    median_height = round(np.median(heights), 4)
    print(f"median height for {serotype}, {region}: {median_height}")
    
    os.makedirs(serotype, exist_ok=True)
    common_tree_file = os.path.join(serotype, f"{serotype}_{region}_commontrees.txt")
    heights_file = os.path.join(serotype, f"{serotype}_{region}_heights.txt")
    
    with open(common_tree_file, 'w') as file:
        file.write("\n".join(subtrees) + "\n")
    
    with open(heights_file, 'w') as file:
        file.write("\n".join(map(str, heights)) + "\n")
    
    with open(args.output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([serotype, "P1", region, median_height])
