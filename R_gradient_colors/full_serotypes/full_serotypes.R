library('ggtree')
library(ggplot2)
library('phytools')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/full_serotypes")

#source("add_gradient_colors.R")
source("../modified_gradients.R")

tree = read.tree("VP1.treefile")
tree_rooted = midpoint.root(tree)

info = read.csv("../metadata.csv")

t = ggtree(tree_rooted, size=0.1) + geom_tiplab(size =0.2)
t

t = ggtree(tree_rooted, size=0.1) %<+% info + geom_tiplab(size = 2, aes(color=serotype)) +
  geom_text(aes(label=node), hjust=-.3, size=0.2)
t 

write.table(get_taxa_name(t, 1523),file="tree_order_1523.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 1526),file="tree_order_1526.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 1814),file="tree_order_1814.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 1831),file="tree_order_1831.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 1956),file="tree_order_1956.csv",col.names=F, row.names=F)
write.table(get_taxa_name(t, 2096),file="tree_order_2096.csv",col.names=F, row.names=F)

taxa_2117 <- get_taxa_name(t, 2117)
taxa_2117
taxa_2201 <- get_taxa_name(t, 2201)
taxa_2201
all_taxa <- c(taxa_2117, taxa_2201)
write.table(all_taxa, file="tree_order_2117_2201.csv", col.names=F, row.names=F)

info_upd = add_colors2meta("order_files.txt", "../metadata.csv")
info_upd = info_upd %>% arrange(GBAC)
#write.csv(info_upd, "metadata_upd_full.csv",row.names=F)

t = ggtree(tree_rooted, size=0.1) %<+% info_upd + 
  geom_text2(aes(label = label, 
                 subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
             size = 0.5, color = "black") +  
  
  geom_tiplab(size = 1, aes(color=label)) +
  
  geom_cladelab(node = 1523, label = "O", align = T,  
                offset = 0.2, textcolor = 'red', barcolor = 'red') +
  geom_cladelab(node = 1526, label = "A", align = T, 
                offset = 0.2, textcolor = 'blue', barcolor = 'blue') +
  geom_cladelab(node = 1814, label = "C", align = T, 
                offset = 0.2, textcolor = 'green', barcolor = 'green') +
  geom_cladelab(node = 1831, label = "Asia1", align = T, 
                offset = 0.2, textcolor = 'pink', barcolor = 'pink') +
  geom_cladelab(node = 1956, label = "SAT2", align = T, 
                offset = 0.2, textcolor = 'cyan', barcolor = 'cyan') +
  geom_cladelab(node = 2096, label = "SAT3", align = T, 
                offset = 0.2, textcolor = 'orange', barcolor = 'orange') +
  geom_strip("OM562535/KEN/cow/2016/SAT1","MH053323/TCD/cattle/1972/SAT1",
             label = "SAT1", align = T, offset = 0.2, color = 'purple', barcolor = 'purple', offset.text=.01) +
  
  coord_cartesian(xlim = c(0, max(tree_rooted$edge.length) + 1)) +
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
    
    geom_tiplab(size = 1, aes(color=label)) +
    
    scale_color_manual(values=info$color) + 
    theme(legend.position = "none") +
    xlim_expand(2, panel = 'label')
  
  return(t)
  
}

# Then you can get the list of trees in a specific directory (working directory in this example)
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_full.csv"
# Create visualization in a loop
for (file in trees){
  # plot tree without legend, add title to plot
  g = plot_tree(file,
                meta_path)  +
    ggtitle(strsplit(strsplit(file, '/')[[1]][2], '.treefile')[[1]][1])
  
  # Construct full file paths
  png_file <- paste0("Images/Gradient/", basename(file), ".png")
  svg_file <- paste0("Images/Gradient/", basename(file), ".svg")
  
  # Save figures
  ggsave(png_file, g, height = 10, width = 7, dpi = 600)
  ggsave(svg_file, g, height = 10, width = 7, dpi = 300)
}

