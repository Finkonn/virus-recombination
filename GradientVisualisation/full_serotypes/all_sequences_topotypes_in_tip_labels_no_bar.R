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

trees = list.files(path = "all_sequences_treefiles/", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_all_sequences.csv"
info = read.csv(meta_path)

unique_serotypes <- unique(info$serotype)
unique_topotypes <- unique(info$Topotype) 
unique_lineages <- unique(info$lineage)
n_lineages <- length(unique_lineages)
n_topotypes <- length(unique_topotypes)

serotype_colors <- setNames(c("#b0b006","#d84a1c" ,"#43998c", "#857fa9","#9ec744", "#d3973f", "#6194b5"), 
                            unique_serotypes)

lineage_colors <- c(
  "#7FC97F", "#BEAED4", "#FDC086", "#FFFF99", "#321faf", 
  "#F0027F", "#BF5B17", "#842f16", "#1B9E77", "#A1aa00",
  "#7570B3", "#5168EE", "#66A6fE"
)

topotype_colors <- c(
  "#FF7F00", "#A6761D", "#A6CEE3", "#1F78B4", "#c90303",
  "#33A02C", "#FB9A99", "#1111ff", "#FDBF6F", "#E6AB02",
  "#CAB2D6", "#6A3D9A", "#B15928", "#8000FF", "#B3CDE3",
  "#bbE535", "#FFFF00", "#A9A2F9", "#2FaFCC", "#A1D2AD",
  "#FDDAEC", "#F2a2F2", "#a1f8aa", "#FDCDAC", "#1EA5E8",
  "#00FFFF", "#E6F5C9", "#FF0080", "#32CD32", "#fa31f1",
  "#f14e2f"
)


names(lineage_colors) <- unique_lineages
names(topotype_colors) <- unique_topotypes



plot_tree_with_gradient_and_heatmap = function(tree_file, meta, serotype_colors, topotype_colors, lineage_colors) {
  tree = read.tree(tree_file)
  tree_rooted = midpoint.root(tree)
  
  info = read.csv(meta)
  
  info$Topotype <- case_when(
    info$Topotype == "EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH" ~ "EURO-SA",
    info$Topotype == "EAST-AFRICA-1-EA-1" ~ "EA-1",
    info$Topotype == "EAST-AFRICA-2-EA-2" ~ "EA-2",
    info$Topotype == "EAST-AFRICA-3-EA-3" ~ "EA-3",
    info$Topotype == "EAST-AFRICA-4-EA-4" ~ "EA-4",
    info$Topotype == "I-NORTHWEST-ZIMBABWE-NWZ" ~ "I-NWZ",
    info$Topotype == "I-SOUTHEAST-ZIMBABWE-SEZ" ~ "I-SEZ",
    info$Topotype == "III-NORTHWEST-ZIMBABWE-NWZ" ~ "III-NWZ",
    info$Topotype == "II-WESTERN-ZIMBABWE-WZ" ~ "II-WZ",
    info$Topotype == "III-WESTERN-ZIMBABWE-WZ" ~ "III-WZ",
    info$Topotype == "INDONESIA-1-ISA-1-1" ~ "ISA-1",
    info$Topotype == "IV-EAST-AFRICA1-EA-1" ~ "IV-EA-1",
    info$Topotype == "MIDDLE-EAST-SOUTH-ASIA-ME-SA" ~ "ME-SA",
    info$Topotype == "V-East-Africa-EA" ~ "V-EA",
    info$Topotype == "VII-EAST-AFRICA-2-EA-2" ~ "VII-EA-2",
    info$Topotype == "WEST-AFRICA-WA" ~ "WA",
    info$Topotype == "SOUTHEAST-ASIA-SEA" ~ "SEA",
    info$Topotype == "EUROPE-SOUTH-AMERICA-EURO-SA" ~ "EURO-SA",
    TRUE ~ info$Topotype
  )
  
  unique_topotypes_abbreviated <- unique(info$Topotype)
  topotype_colors_abbreviated <- topotype_colors
  names(topotype_colors_abbreviated) <- sapply(names(topotype_colors), function(x) {
    case_when(
      x == "EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH" ~ "EURO-SA",
      x == "EAST-AFRICA-1-EA-1" ~ "EA-1",
      x == "EAST-AFRICA-2-EA-2" ~ "EA-2",
      x == "EAST-AFRICA-3-EA-3" ~ "EA-3",
      x == "EAST-AFRICA-4-EA-4" ~ "EA-4",
      x == "I-NORTHWEST-ZIMBABWE-NWZ" ~ "I-NWZ",
      x == "I-SOUTHEAST-ZIMBABWE-SEZ" ~ "I-SEZ",
      x == "III-NORTHWEST-ZIMBABWE-NWZ" ~ "III-NWZ",
      x == "II-WESTERN-ZIMBABWE-WZ" ~ "II-WZ",
      x == "III-WESTERN-ZIMBABWE-WZ" ~ "III-WZ",
      x == "INDONESIA-1-ISA-1-1" ~ "ISA-1",
      x == "IV-EAST-AFRICA1-EA-1" ~ "IV-EA-1",
      x == "MIDDLE-EAST-SOUTH-ASIA-ME-SA" ~ "ME-SA",
      x == "V-East-Africa-EA" ~ "V-EA",
      x == "VII-EAST-AFRICA-2-EA-2" ~ "VII-EA-2",
      x == "WEST-AFRICA-WA" ~ "WA",
      x == "SOUTHEAST-ASIA-SEA" ~ "SEA",
      x == "EUROPE-SOUTH-AMERICA-EURO-SA" ~ "EURO-SA",
      TRUE ~ x
    )
  })
  
  heat_data = data.frame(
    "serotype" = info$serotype,
    "Topotype" = info$Topotype,
    "Lineage" = info$lineage
  )
  rownames(heat_data) <- info$GBAC
  
  info$label_with_topotype <- paste0(info$GBAC, " [", info$Topotype, "]")
  
  t = ggtree(tree_rooted, size = 0.1) %<+% info +
    geom_point2(aes(label=label, 
                    subset = !is.na(as.numeric(label)) & as.numeric(label) < 95), size=0.1, color="red",alpha=0.5) +
    geom_tiplab(aes(label=label_with_topotype, color=label), size = 0.2) +
    scale_color_manual(values=info$color, guide='none') + 
    theme(legend.position = "none") +
    theme_tree2()
  
  return(t)
}


for (file in trees) {
  g = plot_tree_with_gradient_and_heatmap(file, meta_path, serotype_colors, topotype_colors, lineage_colors) +
    ggtitle(strsplit(basename(file), '.treefile')[[1]][1]) +
    guides(
      fill = guide_legend(
        ncol = 1,
        keywidth = unit(0.1, "cm"),
        keyheight = unit(0.1, "cm"),
        override.aes = list(size = 2)
      )
    ) +
    theme(
      legend.text = element_text(size = 14),
      legend.title = element_text(size = 18)
    )
  
  legend <- cowplot::get_legend(g)
  g_nolegend <- g + theme(legend.position = "none")
  
  pdf_file <- paste0("all_sequences_plots/topotypes_in_tip_labels/", basename(file), "_no_bar_shrinked.pdf")
  
  ggsave(pdf_file, g_nolegend, height = 20, width = 2)
  
  
}

ggsave(paste0("all_sequences_plots/topotypes_in_tip_labels/", basename(file), "_legend.png"), 
       plot = legend, height = 10, width = 7, dpi = 600)
ggsave(paste0("all_sequences_plots/topotypes_in_tip_labels/", basename(file), "_legend.svg"), 
       plot = legend, height = 10, width = 7, dpi = 600)

