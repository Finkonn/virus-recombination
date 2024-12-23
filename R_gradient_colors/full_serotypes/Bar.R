library('ggtree')
library('ggplot2')
library('phytools')
library('dplyr')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/full_serotypes")

source("../modified_gradients.R")

tree = read.tree("VP1.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

unique_serotypes <- unique(info$serotype)
serotype_colors <- setNames(c("red", "blue", "green", "purple", "orange", "cyan", "pink"), 
                            unique_serotypes)

plot_tree_with_heatmap = function(tree_file, meta, serotype_colors){
  
  tree =  read.tree(tree_file)
  tree_rooted = midpoint.root(tree)
  
  info = read.csv(meta)
  
  serotypes = data.frame("serotypes" = info[,c("serotype")])
  rownames(serotypes) <- info$GBAC
  
  t = ggtree(tree_rooted, size=0.1) %<+% info +
    geom_tiplab(size = 0.5, aes(color=serotype)) +
    scale_color_manual(values=serotype_colors, guide="none") +
    theme(legend.position = "right")
  
  t = gheatmap(t, serotypes,                           
               offset = 0.2,                  
               width = 0.1,                        
               colnames_position = "top",         
               colnames_angle = 0,                  
               colnames_offset_y = 20, 
               color = NULL) +
    scale_fill_manual(values=serotype_colors, name = "Serotype")
  return(t)
}

trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "../metadata.csv"

for (file in trees){
  g = plot_tree_with_heatmap(file, meta_path, serotype_colors) +
    ggtitle(strsplit(basename(file), '.treefile')[[1]][1])
  
  png_file <- paste0("Images/Heatbar/", basename(file), "_heatmap.png")
  svg_file <- paste0("Images/Heatbar/", basename(file), "_heatmap.svg")
  
  ggsave(png_file, g, height = 10, width = 7, dpi = 600)
  ggsave(svg_file, g, height = 10, width = 7, dpi = 300)
}

