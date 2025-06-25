library(ggtree)
library(treeio)
library(ape)
library(tidyr)
library(ggpubr)
library(ggplot2)
library(stringr)

setwd("C:/Users/Mate_/Downloads/compare_trees_RF")
source("get_subtrees.R")

regions2 = c("Lpro", "P2", "P3")

tree1_files = list.files("MCMC", pattern = "\\.tree$", full.names = TRUE)

for (tree1_path in tree1_files) {
  
  tree1_file = basename(tree1_path)          
  base_name = tools::file_path_sans_ext(tree1_file)  
  parts = str_split(base_name, "_", simplify = TRUE)
  serotype = parts[1]
  region1 = parts[2]
  
  tree1 = read.beast(tree1_path)
  
  for (region2 in regions2) {
    tree2_path = file.path(region2, paste0(serotype, ".fasta.treefile"))
    if (!file.exists(tree2_path)) next
    tree2 = read.tree(tree2_path)
    
    for (suffix in c("commontrees.txt", "commontrees_bip.txt")) {
      
      subtree_dir = paste0(serotype, "_", region2)
      subtree_file = file.path(subtree_dir, paste0(base_name, "_", serotype, ".fasta_", suffix))
      if (!file.exists(subtree_file)) next
      
      subtrees = get_subtrees(subtree_file)
      
      # Построение дерева 1
      p1 = ggtree(tree1, mrsd = "2025-01-01", size = 0.3) + 
        geom_tiplab(size = 1) + 
        geom_point2(aes(subset = !is.na(as.numeric(posterior)) & as.numeric(posterior) > 0.9), 
                    shape = 21, fill = "blue", color = "black", size = 0.5) +
        theme_tree2()
      p1 = groupOTU(p1, subtrees, 'Clade') + aes(color = Clade) +
        scale_color_manual(values = c("black", "firebrick")) + 
        coord_cartesian(clip = "off") +
        theme_tree2(plot.margin = margin(5, 60, 5, 5), legend.position = "none")
      
      # Построение дерева 2
      p2 = ggtree(tree2, size = 0.3) +  
        geom_tiplab(size = 1) + 
        geom_point2(aes(subset = !is.na(as.numeric(label)) & as.numeric(label) > 90), 
                    shape = 21, fill = "blue", color = "black", size = 0.5) +
        theme_tree2()
      p2 = groupOTU(p2, subtrees, 'Clade') + aes(color = Clade) +
        scale_color_manual(values = c("black", "firebrick")) +
        coord_cartesian(clip = "off") +
        theme_tree2(plot.margin = margin(5, 60, 5, 5), legend.position = "none")
      
      # Заголовок по типу файла
      plot_type = ifelse(grepl("bip", suffix), "bipartitions", "subtrees")
      plot_title = paste(serotype, "-", region2, plot_type)
      
      plot_combined = ggarrange(p1, p2)
      plot_combined = annotate_figure(plot_combined, top = text_grob(plot_title, face = "bold", size = 14))
      
      # Сохранение
      out_dir = file.path("Plots", serotype, paste0(region1, "_", region2))
      dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
      plot_name = tools::file_path_sans_ext(suffix)
      out_base = file.path(out_dir, paste0(base_name, "_", serotype, "_", region2, "_", plot_name))
      
      ggsave(paste0(out_base, ".png"), plot_combined, width = 10, height = 5, dpi = 300, bg = "white")
      ggsave(paste0(out_base, ".svg"), plot_combined, width = 10, height = 5)
    }
    
  }
}
