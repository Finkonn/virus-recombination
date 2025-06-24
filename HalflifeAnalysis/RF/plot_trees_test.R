library(ggtree)
library(treeio) #read.beast
library(ape) # for phylo objects
library(tidyr)
library(ggpubr)

# set  working directory
#setwd("")
# Load functions from source code
source("get_subtrees.R")

# Example 1. The nexus trees, leaf sets are different. 
#The set of leaves in one tree is a subset of the leaves in another tree

# converts file with common subtrees in newick format into list with taxa names
# *_commontrees.txt" is a file with common subtrees between two phylogenetic trees
# Each subtree is in newick format
# this file is output of get_RF_halflife.py
# Example: python.exe .\get_RF_halflife.py -tree1 .\norovirus_vp1.tree -tree2 .\norovirus_rdrp_g2.tree

subtrees = get_subtrees("result/O_bayes_lognormal_400mil_limited-O_O0.fasta_commontrees.txt")

# Path to file with tree in nexus format produced by BEAST
tree1_name = "O_bayes_lognormal_400mil_limited-O.tree"
tree1 = read.beast(tree1_name)

tree2_name = "O0.fasta.treefile"
tree2 = read.tree(tree2_name)

# Plot beast subtree and color braches of common subtrees
p1 = ggtree(tree1,mrsd="2025-01-01") +  geom_tiplab(size=2) + 
            geom_label2(aes(label=round(as.numeric(posterior),2)),size=2)
p1 = groupOTU(p1, subtrees, 'Clade') + aes(color=Clade) +
  theme(legend.position="right") + scale_color_manual(values=c("black", "firebrick"))

p2 = ggtree(tree2,mrsd="2025-01-01") +  geom_tiplab(size=2) + 
            geom_label2(aes(label=round(as.numeric(posterior),2)),size=2)
p2 = groupOTU(p2, subtrees, 'Clade') + aes(color=Clade) +
  theme(legend.position="right") + scale_color_manual(values=c("black", "firebrick"))

ggarrange(p1,p2)

# Example 2. Trees with the same leaf sets


# Path to file with tree in nexus format produced by BEAST
tree1_name = "O_bayes_lognormal_400mil_limited-O.tree"
tree1 = read.beast(tree1_name)

tree2_name = "O0.fasta.treefile"
tree2 = read.tree(tree2_name)

# common subtrees determined from coinciding bipartitions in two trees
subtrees = get_subtrees("result/O_bayes_lognormal_400mil_limited-O_O0.fasta_commontrees.txt")


# Plot BEAST subtree and color branches of common subtrees
p1 = ggtree(tree1, mrsd = "2025-01-01") + 
  geom_tiplab(size = 1) + 
  geom_nodepoint(aes(label = posterior, 
                     subset = !is.na(as.numeric(posterior)) & as.numeric(posterior) >= 80),
                 size = 1, color = "green") +  
  theme_tree2()

p1 = groupOTU(p1, subtrees, 'Clade') + 
  aes(color = Clade) +
  scale_color_manual(values = c("black", "firebrick")) +
  theme(legend.position = "none")  # <-- убираем легенду

p2 = ggtree(tree2) + 
  geom_tiplab(size = 1) + 
  geom_nodepoint(aes(label = label, 
                     subset = !is.na(as.numeric(label)) & as.numeric(label) >= 100),
                 size = 1, color = "green") +  
  theme_tree2()

p2 = groupOTU(p2, subtrees, 'Clade') + 
  aes(color = Clade) +
  scale_color_manual(values = c("black", "firebrick")) +
  theme(legend.position = "none")  # <-- убираем легенду

# Combine plots
ggarrange(p1, p2)

