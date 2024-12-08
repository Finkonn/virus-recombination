library('ggtree')
library(ggplot2)
library('phytools')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/SAT1_topotypes")

#source("add_gradient_colors.R")
source("../modified_gradients.R")

tree = read.tree("VP1_SAT1.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

t = ggtree(tree_rooted, size=0.1) + geom_tiplab(size =0.2)
t

t = ggtree(tree_rooted, size=0.1) %<+% info + geom_tiplab(size = 2, aes(color=Topotype)) +
  geom_text(aes(label=node), hjust=-.3, size=0.2)
t 

write.table(get_taxa_name(t, 100),file="tree_order_100.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 120),file="tree_order_120.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 116),file="tree_order_116.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 114),file="tree_order_114.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 108),file="tree_order_108.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 106),file="tree_order_106.csv",col.names=F, row.names=F)

taxa_5 <- "AY593844/ISR/Unknown/1962/SAT1"
taxa_6 <- "MH053323/TCD/cattle/1972/SAT1"
all_taxa <- c(taxa_5, taxa_6)
write.table(all_taxa, file="tree_order_5_6.csv", col.names=F, row.names=F)

info_upd = add_colors2meta("order_files.txt", "SAT1.csv")
info_upd = info_upd %>% arrange(GBAC)
write.csv(info_upd, "metadata_upd_SAT1.csv",row.names=F)

t = ggtree(tree_rooted, size=0.1) %<+% info_upd + 
  geom_text2(aes(label = label, 
                 subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
             size = 1, color = "black") +  
  
  geom_tiplab(size = 1, aes(color=label)) +
  
  geom_cladelab(node = 100, label = "NWZ", align = T,  
                offset = 0.065, textcolor = 'red', barcolor = 'red') +
  geom_cladelab(node = 120, label = "WZ", align = T, 
                offset = 0.065, textcolor = 'blue', barcolor = 'blue') +
  geom_cladelab(node = 116, label = "ASIA", align = T, 
                offset = 0.065, textcolor = 'green', barcolor = 'green') +
  geom_cladelab(node = 114, label = "EA-1", align = T, 
                offset = 0.065, textcolor = 'pink', barcolor = 'pink') +
  geom_cladelab(node = 108, label = "X", align = T, 
                offset = 0.065, textcolor = 'cyan', barcolor = 'cyan') +
  geom_cladelab(node = 106, label = "EA-2", align = T, 
                offset = 0.065, textcolor = 'orange', barcolor = 'orange') +
  geom_strip("AY593844/ISR/Unknown/1962/SAT1","MH053323/TCD/cattle/1972/SAT1",
             label = "VI", align = T, offset = 0.065, color = 'purple', barcolor = 'purple') +
  
  coord_cartesian(xlim = c(0, max(tree_rooted$edge.length) + 0.15)) +
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
    xlim_expand(1, panel = 'label')
  
  return(t)
  
}

# Then you can get the list of trees in a specific directory (working directory in this example)
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_SAT1.csv"
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


