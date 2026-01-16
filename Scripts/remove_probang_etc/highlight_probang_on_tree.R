library(ggtree)
library(treeio)
library(readxl)
library(ggplot2)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

table <- read_excel("meta_no_probang_removed_seqs.xlsx")
accessions <- table$`Genbank accession`

tree_files = list.files(path = "bayes_trees_and_plots/", full.names = TRUE, pattern = "\\.tree$")

for(tree_file in tree_files){
  tree <- read.beast(tree_file)
  
  tip_accessions <- sapply(strsplit(tree@phylo$tip.label,"/"), `[`, 1)
  tip_data <- data.frame(
    label = tree@phylo$tip.label,
    accession = tip_accessions,
    color = ifelse(tip_accessions %in% accessions, "red", "black")
  )
  
  tree@phylo$tip.color <- tip_data$color

  plot_title <- basename(tree_file)
  plot_title <- gsub("\\.tree$", "", plot_title)
  plot_title <- gsub("_", " ", plot_title)  
  plot_title <- gsub("-", " ", plot_title) 
  plot_title <- tools::toTitleCase(plot_title) 
  
  p <- ggtree(tree, size = 0.5, mrsd="2025-01-01") %<+% tip_data +
    geom_tiplab(aes(color=color), show.legend = FALSE, size = 1.5) + 
    theme_tree2() +
    scale_color_identity() +
    ggtitle(plot_title) +  # Add the title
    theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"))  
  
  base_name <- gsub("\\.tree$", "", tree_file)
  ggsave(paste0(base_name, "_colored.png"), p, width = 20, height = 14, dpi = 600)
  ggsave(paste0(base_name, "_colored.svg"), p, width = 16, height = 14)
}