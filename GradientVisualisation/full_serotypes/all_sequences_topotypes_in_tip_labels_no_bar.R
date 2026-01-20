library('ggtree')
library('ggplot2')
library('phytools')
library('dplyr')
library('ggnewscale')
library('cowplot')
library('ape')
library('RColorBrewer')
library('randomcoloR')

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
source("../modified_gradients.R")

trees = list.files(path = "no_probang_trees/", full.names = TRUE, pattern = ".treefile$")
meta_path = "meta_no_probang_with_GBAC_upd_test.csv"
info = read.csv(meta_path)

plot_tree_with_gradient_and_heatmap = function(tree_file, meta, serotype_colors, topotype_colors, lineage_colors) {
  tree = read.tree(tree_file)
  tree_rooted = midpoint.root(tree)
  
  info = read.csv(meta)
  
  info$label_with_topotype <- ifelse(
    is.na(info$pool) | info$pool == "",
    sub("/[^/]*$", "", info$GBAC),
    paste(
      sub("/[^/]*$", "", info$GBAC),
      paste0("[", sub("/.*", "", info$pool), "]"),
      sep = " "
    )
  )
  
  t = ggtree(tree_rooted, size = 0.2) %<+% info +
    geom_point2(aes(label=label, 
                    subset = !is.na(as.numeric(label)) & as.numeric(label) > 95), size=0.1, color="black",alpha=0.8) +
    geom_tiplab(aes(label=label_with_topotype, color=label), size = 0.2) +
    scale_color_manual(values=info$color, guide='none') + 
    theme(legend.position = "none") +
    theme_tree()
  
  return(t)
}

region_letters <- list(
  "Lpro" = "A",
  "P1"   = "B",
  "P2"   = "C",
  "P3"   = "D"
)

for (file in trees) {
  
  file_base <- strsplit(basename(file), ".treefile")[[1]][1]
  
  region_titles <- list(
    "Lpro" = "Region L",
    "P1"   = "Region P1",
    "P2"   = "Region P2",
    "P3"   = "Region P3"
  )
  
  region_key <- names(region_titles)[sapply(names(region_titles), function(x) grepl(x, file_base, ignore.case = TRUE))]
  region_title <- ifelse(length(region_key) == 1, region_titles[[region_key]], file_base)
  
  g = plot_tree_with_gradient_and_heatmap(
    file, meta_path, serotype_colors, topotype_colors, lineage_colors
  )
  
  plot_letter <- ifelse(
    length(region_key) == 1,
    region_letters[[region_key]],
    ""
  )
  
  g_nolegend <- g +
    ggtitle(plot_letter) +
    theme(
      legend.position = "none",
      plot.title = element_text(
        hjust = 0,        # left aligned
        size = 32
      ),
      plot.title.position = "plot"
    )
  
  #pdf_file <- paste0("Plots/no_probang/topotypes_in_tip_labels/", basename(file), "_no_bar_labeled_test.pdf")
  #ggsave(pdf_file, g_nolegend, height = 20, width = 12)
  pdf_file <- paste0("Plots/no_probang/topotypes_in_tip_labels//", basename(file), "_no_bar_shrinked.pdf")
  ggsave(pdf_file, g_nolegend, height = 20, width = 8)
  
}

#ggsave(paste0("all_sequences_plots/topotypes_in_tip_labels/", basename(file), "_legend.png"), 
#       plot = legend, height = 10, width = 7, dpi = 600)
#ggsave(paste0("all_sequences_plots/topotypes_in_tip_labels/", basename(file), "_legend.svg"), 
#       plot = legend, height = 10, width = 7, dpi = 600)

