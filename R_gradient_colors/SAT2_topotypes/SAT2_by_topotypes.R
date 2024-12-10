library('ggtree')
library(ggplot2)
library('phytools')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/SAT2_topotypes")

#source("add_gradient_colors.R")
source("../modified_gradients.R")

tree = read.tree("VP1_SAT2.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

t = ggtree(tree_rooted, size=0.1) + geom_tiplab(size =0.2)
t

t = ggtree(tree_rooted, size=0.1) %<+% info + geom_tiplab(size = 2, aes(color=Topotype)) +
  geom_text(aes(label=node), hjust=-.3, size=0.2)
t 

write.table(get_taxa_name(t, 177),file="tree_order_177.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 278),file="tree_order_278.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 144),file="tree_order_144.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 175),file="tree_order_175.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 149),file="tree_order_149.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 153),file="tree_order_153.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 173),file="tree_order_173.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 174),file="tree_order_174.csv",col.names=F, row.names=F)

info_upd = add_colors2meta("order_files.txt", "SAT2.csv")
info_upd = info_upd %>% arrange(GBAC)
write.csv(info_upd, "metadata_upd_SAT2.csv",row.names=F)

t = ggtree(tree_rooted, size=0.1) %<+% info_upd + 
  geom_text2(aes(label = label, 
                 subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
             size = 1, color = "black") +  
  
  geom_tiplab(size = 1, aes(color=label)) +
  
  geom_cladelab(node = 177, label = "IV", align = T,  
                offset = 0.072, textcolor = 'red', barcolor = 'red') +
  geom_cladelab(node = 278, label = "III", align = T, 
                offset = 0.072, textcolor = 'blue', barcolor = 'blue', fontsize=3) +
  geom_cladelab(node = 144, label = "I", align = T, 
                offset = 0.072, textcolor = 'green', barcolor = 'green', fontsize=2) +
  geom_cladelab(node = 175, label = "II", align = T, 
                offset = 0.072, textcolor = 'pink', barcolor = 'pink', fontsize=2) +
  geom_cladelab(node = 149, label = "X", align = T, 
                offset = 0.072, textcolor = 'cyan', barcolor = 'cyan', fontsize=2) +
  geom_cladelab(node = 153, label = "VII", align = T, 
                offset = 0.072, textcolor = 'orange', barcolor = 'orange') +
  geom_cladelab(node = 173, label = "XIV", align = T, 
                offset = 0.072, textcolor = 'purple', barcolor = 'purple', fontsize=2) +
  geom_cladelab(node = 174, label = "IX", align = T, 
                offset = 0.072, textcolor = 'lightblue', barcolor = 'lightblue', fontsize=2) +
  
  coord_cartesian(xlim = c(0, max(tree_rooted$edge.length) + 0.3)) +
  scale_color_manual(values=info_upd$color) + 
  theme(legend.position = "none")
t


#' Function to plot the phylogenetic tree
#' @param tree_file  path to tree file in nwk format
#' @param meta  path to table with metadata
#' @return ggtree object

plot_tree = function(tree_file, meta){
  
  tree =  read.tree(tree_file)
  # root by midpoint
  tree_rooted = midpoint.root(tree)
  # read csv file with metadata
  info = read.csv(meta)
  
  t = ggtree(tree_rooted, size=0.1) %<+% info + 
    geom_text2(aes(label = label, 
                   subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
               size = 1, color = "black") +  
    
    geom_tiplab(size = 2, aes(color=label)) +
    
    scale_color_manual(values=info$color) + 
    theme(legend.position = "none") +
    xlim_expand(2.5, panel = 'label')
  
  return(t)
  
}

# Then you can get the list of trees in a specific directory (working directory in this example)
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_SAT2.csv"
# Create visualization in a loop
for (file in trees){
  # plot tree without legend, add title to plot
  g = plot_tree(file,
                meta_path)  +
    ggtitle(strsplit(strsplit(file, '/')[[1]][2], '.treefile')[[1]][1])
  
  # Construct full file paths
  png_file <- paste0("Images/", basename(file), ".png")
  svg_file <- paste0("Images/", basename(file), ".svg")
  
  # Save figures
  ggsave(png_file, g, height = 10, width = 7, dpi = 600)
  ggsave(svg_file, g, height = 10, width = 7, dpi = 300)
}


