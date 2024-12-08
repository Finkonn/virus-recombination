library('ggtree')
library(ggplot2)
library('phytools')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/SAT3_topotypes")

#source("add_gradient_colors.R")
source("../modified_gradients.R")

tree = read.tree("VP1_SAT3.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

t = ggtree(tree_rooted, size=0.1) + geom_tiplab(size =0.2)
t

t = ggtree(tree_rooted, size=0.1) %<+% info + geom_tiplab(size = 2, aes(color=Topotype)) +
  geom_text(aes(label=node), hjust=-.3, size=0.2)
t 

write.table(get_taxa_name(t, 27),file="tree_order_27.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 25),file="tree_order_25.csv",col.names=F, row.names=F)

taxa_16 <- "MH053343/ZWE/cattle/1934/SAT3"
taxa_15 <- "MH053352/ZWE/african-buffalo/1990/SAT3"
taxa_13 <- "MW355678/ZMB/african-buffalo/1996/SAT3"
all_taxa <- c(taxa_16, taxa_15, taxa_13)
write.table(all_taxa, file="tree_order_16_15_13.csv", col.names=F, row.names=F)

taxa_14 <- "KJ820999/UGA/cattle/2013/SAT3"
write.table(taxa_14, file="tree_order_14.csv", col.names=F, row.names=F)


info_upd = add_colors2meta("order_files.txt", "SAT3.csv")
info_upd = info_upd %>% arrange(GBAC)
write.csv(info_upd, "metadata_upd_SAT3.csv",row.names=F)

t = ggtree(tree_rooted, size=0.1) %<+% info_upd + 
  geom_text2(aes(label = label, 
                 subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
             size = 1, color = "black") +  
  
  geom_tiplab(size = 1, aes(color=label)) +
  
  geom_cladelab(node = 27, label = "SEZ", align = T,  
                offset = 0.09, textcolor = 'red', barcolor = 'red') +
  
  geom_cladelab(node = 25, label = "WZ", align = T, 
                offset = 0.09, textcolor = 'blue', barcolor = 'blue') +
  
  geom_strip("MH053343/ZWE/cattle/1934/SAT3", "MW355678/ZMB/african-buffalo/1996/SAT3", 
             label = "NWZ", align = T, offset = 0.09, color = 'green', barcolor = 'green') +
  
  geom_cladelab(node = 14, label = "EA", align = T, offset = 0.09,
                textcolor = 'cyan', barcolor = 'cyan') +
  
  coord_cartesian(xlim = c(0, max(tree_rooted$edge.length) + 0.12)) +
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
meta_path = "metadata_upd_SAT3.csv"
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


