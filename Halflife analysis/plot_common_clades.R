library(ggtree)
library(treeio)
library(ape)
library(tidyr)
library(ggpubr)

source("get_subtrees.R")

serotypes = c("A", "Asia1", "C", "O", "SAT1", "SAT2", "SAT3")
regions = c("Lpro", "P1", "P2", "P3")

for (serotype in serotypes) {
  for (region in regions) {
    
    commontree_file = file.path(serotype, paste0(serotype, "_", region, "_commontrees.txt"))
    tree1_file = file.path("MCC", paste0(serotype, "_P1.tree"))
    tree2_file = file.path(region, paste0(serotype, ".treefile"))
    output_dir = file.path("Plots", serotype)
    
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
      geom_tiplab(size=1) +  
      geom_label2(aes(label=round(as.numeric(posterior),2)), size=1) +
      theme(plot.margin=margin(6, 40, 6, 6), legend.position="none") + coord_cartesian(clip='off')
    
    p2 = ggtree(tree2, size=0.1)
    p2 = groupOTU(p2, subtrees, "Clade") + aes(color = Clade) +
      scale_color_manual(values=c("black", "firebrick")) +
      geom_label2(aes(label=as.numeric(label)), size=1) +
      geom_tiplab(size=1) +
      theme(plot.margin=margin(6, 40, 6, 6), legend.position="none") + coord_cartesian(clip='off')
    
    final_plot = ggarrange(p1, p2)
    
    # Сохраняем в PDF и SVG
    pdf_path = file.path(output_dir, paste0(serotype, "_", region, ".pdf"))
    svg_path = file.path(output_dir, paste0(serotype, "_", region, ".svg"))
    
    ggsave(pdf_path, final_plot, width=10, height=5)
    ggsave(svg_path, final_plot, width=10, height=5)
    
    print(paste("Файлы сохранены:", pdf_path, "и", svg_path))
  }
}

print("Анализ завершен!")
