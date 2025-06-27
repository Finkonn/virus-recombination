library(ggtree)
library(treeio) #read.beast
library(ape) # for phylo objects
library(tidyr)
library(ggpubr)
library(phytools)

# set  working directory
setwd("C:/Users/Mate_/Downloads/compare_trees_RF")
# Load functions from source code
source("get_subtrees.R")

# Example 1. The nexus trees, leaf sets are different. 
#The set of leaves in one tree is a subset of the leaves in another tree

# converts file with common subtrees in newick format into list with taxa names
# *_commontrees.txt" is a file with common subtrees between two phylogenetic trees
# Each subtree is in newick format
# this file is output of get_RF_halflife.py
# Example: python.exe .\get_RF_halflife.py -tree1 .\norovirus_vp1.tree -tree2 .\norovirus_rdrp_g2.tree

subtrees = get_subtrees("Asia1_Lpro/Asia1_P1_Asia1.fasta_commontrees.txt")

# Path to file with tree in nexus format produced by BEAST
tree1_name = "MCMC/Asia1_P1.tree"
tree1 = read.beast(tree1_name)

tree2_name = "Lpro/Asia1.fasta.treefile"
tree2 = read.tree(tree2_name)

# Plot beast subtree and color braches of common subtrees
p1 = ggtree(tree1,mrsd="2025-01-01") +  geom_tiplab(size=2) + 
            geom_label2(aes(label=round(as.numeric(posterior),2)),size=2)
p1 = groupOTU(p1, subtrees, 'Clade') + aes(color=Clade) +
  theme(legend.position="right") + scale_color_manual(values=c("black", "firebrick"))

p2 = ggtree(tree2,mrsd="2025-01-01") +  geom_tiplab(size=2) + 
            geom_label2(aes(label=round(as.numeric(label),2)),size=2)
p2 = groupOTU(p2, subtrees, 'Clade') + aes(color=Clade) +
  theme(legend.position="right") + scale_color_manual(values=c("black", "firebrick"))

ggarrange(p1,p2)

# Example 2. Trees with the same leaf sets

# Path to file with tree in nexus format produced by BEAST
tree1_name = "MCMC/Asia1_P1.tree"
tree1 = read.beast(tree1_name)

tree2_name = "Lpro/Asia1.fasta.treefile"
tree2 = read.tree(tree2_name)
tree2 = midpoint.root(tree2)


# common subtrees determined from coinciding bipartitions in two trees
subtrees = get_subtrees("Asia1_Lpro/Asia1_P1_Asia1.fasta_commontrees_bip.txt")

p1 = ggtree(tree1, mrsd = "2025-01-01", size = 0.3) + geom_tiplab(size = 1) + 
  geom_point2(aes(subset = !is.na(as.numeric(posterior)) & as.numeric(posterior) > 0.9), 
              shape = 21, fill = "blue", color = "black", size = 0.5) +
  theme_tree2()
  

p1 = groupOTU(p1, subtrees, 'Clade') + aes(color = Clade) +
  scale_color_manual(values = c("black", "firebrick")) + 
  coord_cartesian(clip = "off") +
  theme_tree2(plot.margin = margin(5, 60, 5, 5), legend.position = "none")

p2 = ggtree(tree2, size = 0.3) +  
  geom_tiplab(size = 1) + 
  geom_point2(aes(subset = !is.na(as.numeric(label)) & as.numeric(label) > 90), 
              shape = 21, fill = "blue", color = "black", size = 0.5) +
  theme_tree2()

p2 = groupOTU(p2, subtrees, 'Clade') + aes(color = Clade) +
  scale_color_manual(values = c("black", "firebrick")) +
  coord_cartesian(clip = "off") +
  theme_tree2(plot.margin = margin(5, 60, 5, 5), legend.position = "none")

plot = ggarrange(p1, p2)

annotate_figure(plot, top = text_grob("Lpro subtrees", face = "bold", size = 14))
