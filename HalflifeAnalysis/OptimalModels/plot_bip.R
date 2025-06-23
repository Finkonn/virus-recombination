library(ggtree)
library(treeio)
library(ape)
library(tidyr)
library(ggpubr)

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/HalflifeAnalysis/OptimalModel")

source("get_subtrees.R")

serotypes = c("Asia1", "O", "SAT1")
regions = c("Lpro", "P1", "P2", "P3")

for (serotype in serotypes) {
  for (region in regions) {
    
    commontree_file = file.path("Results", serotype, paste0(serotype, "_", region, "_commontrees_bip.txt"))
    tree1_file = file.path("MCC", paste0(serotype, "_P1.tree"))
    tree2_file = file.path(region, paste0(serotype, ".treefile"))
    output_dir = file.path("Plots/bip", serotype)
    
    print(paste("Обрабатываем:", serotype, region))
    print(paste("Файл общих клад:", commontree_file))
    print(paste("BEAST-дерево:", tree1_file))
    print(paste("ML-дерево:", tree2_file))
    
    if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
    
    tree1 = read.beast(tree1_file)
    tree2 = read.tree(tree2_file)
    
    subtrees = get_subtrees(commontree_file)
    
    # Строим деревья
    p1 = ggtree(tree1, mrsd="2025-01-01", size=0.1) 
    p1 = groupOTU(p1, subtrees, "Clade") + aes(color = Clade) +
      scale_color_manual(values=c("black", "firebrick")) +
      geom_tiplab(size=1, show.legend=FALSE) +
      geom_nodepoint(aes(size = posterior), shape=21, fill="gray20", show.legend=FALSE) +
      scale_size_continuous(range = c(0.2, 1), limits=c(0.5, 1)) +
      theme(plot.margin=margin(6, 40, 6, 6), legend.position="none") +
      coord_cartesian(clip='off') +
      theme_tree2()
    
    p2 = ggtree(tree2, size=0.1)
    p2 = groupOTU(p2, subtrees, "Clade") + aes(color = Clade) +
      scale_color_manual(values=c("black", "firebrick")) +
      geom_tiplab(size=1, show.legend=FALSE) +
      geom_nodepoint(aes(size = as.numeric(label)), shape=21, fill="gray20", show.legend=FALSE) +
      scale_size_continuous(range = c(0.2, 1), limits=c(50, 100)) +  # Можно фильтровать <50
      theme(plot.margin=margin(6, 40, 6, 6), legend.position="none") +
      coord_cartesian(clip='off')
    

    
    final_plot = ggarrange(p1, p2)
    
    # Сохраняем в PDF и SVG
    pdf_path = file.path(output_dir, paste0(serotype, "_", region, "_bip.png"))
    svg_path = file.path(output_dir, paste0(serotype, "_", region, "_bip.svg"))
    
    ggsave(pdf_path, final_plot, width=10, height=5, dpi=600)
    ggsave(svg_path, final_plot, width=10, height=5, dpi=600)
    
    print(paste("Файлы сохранены:", pdf_path, "и", svg_path))
  }
}

print("Анализ завершен!")
