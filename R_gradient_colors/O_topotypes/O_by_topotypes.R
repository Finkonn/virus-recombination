library('ggtree')
library(ggplot2)
library('phytools')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/O_topotypes")

#source("add_gradient_colors.R")
source("../modified_gradients.R")

tree = read.tree("VP1_O.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

t = ggtree(tree_rooted, size=0.1) + geom_tiplab(size =0.2)
t

ggtree(tree_rooted, size=0.01) + geom_text(aes(label=node), hjust=-.3, size=0.2)


t = ggtree(tree_rooted, size=0.1) %<+% info + geom_tiplab(size = 0.2, aes(color=Topotype)) +
  geom_text(aes(label=node), hjust=-.3, size=0.2)
t 

write.table(get_taxa_name(t, 834),file="tree_order_834.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 997),file="tree_order_997.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 855),file="tree_order_855.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 839),file="tree_order_839.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 884),file="tree_order_884.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 975),file="tree_order_975.csv",col.names=F, row.names=F)

info_upd = add_colors2meta("order_files.txt", "O.csv")
info_upd = info_upd %>% arrange(GBAC)
write.csv(info_upd, "metadata_upd_O.csv",row.names=F)

t = ggtree(tree_rooted, size=0.1) %<+% info_upd + 
  geom_text2(aes(label = label, 
                 subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
             size = 1, color = "black") +  
  
  geom_tiplab(size = 1, aes(color=label)) +
  
  geom_cladelab(node = 834, label = "ME-SA", align = T,  
                offset = 0.04, textcolor = 'red', barcolor = 'red') +
  geom_cladelab(node = 997, label = "NWZ", align = T, 
                offset = 0.04, textcolor = 'blue', barcolor = 'blue') +
  geom_cladelab(node = 855, label = "EA-3", align = T, 
                offset = 0.04, textcolor = 'green', barcolor = 'green') +
  geom_cladelab(node = 839, label = "EA-2", align = T, 
                offset = 0.04, textcolor = 'pink', barcolor = 'pink') +
  geom_cladelab(node = 884, label = "EURO-SA", align = T, 
                offset = 0.04, textcolor = 'cyan', barcolor = 'cyan') +
  geom_cladelab(node = 975, label = "CATHAY", align = T, 
                offset = 0.04, textcolor = 'orange', barcolor = 'orange') +
  
  coord_cartesian(xlim = c(0, max(tree_rooted$edge.length) + 0.27)) +
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
    xlim_expand(0.5, panel = 'label')
  
  return(t)
  
}

# Then you can get the list of trees in a specific directory (working directory in this example)
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_O.csv"
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


