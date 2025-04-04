library('ggtree')
library('ggplot2')
library('phytools')
library('dplyr')
library('ggnewscale')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/GradientVisualisation/full_serotypes")

source("../modified_gradients.R")

# Список файлов с деревьями
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_full.csv"

# Цвета для серотипов и топотипов
info = read.csv(meta_path)
unique_serotypes <- unique(info$serotype)
serotype_colors <- setNames(c("#B7B718", "#B67603", "#5F93B3", "#BDB9DB", "#D54514", "#3F9588", "#9FC845"), 
                            unique_serotypes)

# Create colors for topotypes (adjust colors as needed)
unique_topotypes <- unique(info$Topotype)  # Note capital T
topotype_colors <- setNames(rainbow(length(unique_topotypes)), unique_topotypes)

plot_tree_with_gradient_and_heatmap = function(tree_file, meta, serotype_colors, topotype_colors) {
  # Загрузка и корневание дерева
  tree = read.tree(tree_file)
  tree_rooted = midpoint.root(tree)
  
  # Загрузка метаданных
  info = read.csv(meta)
  
  # Create abbreviations for Topotypes
  info$Topotype <- case_when(
    info$Topotype == "EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH" ~ "EURO-SA",
    info$Topotype == "EAST-AFRICA-1-EA-1" ~ "EA-1",
    info$Topotype == "EAST-AFRICA-2-EA-2" ~ "EA-2",
    info$Topotype == "EAST-AFRICA-3-EA-3" ~ "EA-3",
    info$Topotype == "EAST-AFRICA-4-EA-4" ~ "EA-4",
    info$Topotype == "I-NORTHWEST-ZIMBABWE-NWZ" ~ "NWZ",
    info$Topotype == "I-SOUTHEAST-ZIMBABWE-SEZ" ~ "SEZ",
    info$Topotype == "III-NORTHWEST-ZIMBABWE-NWZ" ~ "NWZ",
    info$Topotype == "II-WESTERN-ZIMBABWE-WZ" ~ "WZ",
    info$Topotype == "III-WESTERN-ZIMBABWE-WZ" ~ "WZ",
    info$Topotype == "INDONESIA-1-ISA-1-1" ~ "ISA-1",
    info$Topotype == "IV-EAST-AFRICA1-EA-1" ~ "EA-1",
    info$Topotype == "MIDDLE-EAST-SOUTH-ASIA-ME-SA" ~ "ME-SA",
    info$Topotype == "V-East Africa-EA" ~ "V-EA",
    info$Topotype == "VII-EAST-AFRICA-2-EA-2" ~ "VII-EA-2",
    info$Topotype == "WEST-AFRICA-WA" ~ "WA",
    TRUE ~ info$Topotype  # Keep original if no match
  )
  
  # Update the unique topotypes and colors (keeping the same colors)
  unique_topotypes_abbreviated <- unique(info$Topotype)
  # Use the same colors but with abbreviated names
  topotype_colors_abbreviated <- topotype_colors
  names(topotype_colors_abbreviated) <- sapply(names(topotype_colors), function(x) {
    case_when(
      x == "EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH" ~ "EURO-SA",
      x == "EAST-AFRICA-1-EA-1" ~ "EA-1",
      x == "EAST-AFRICA-2-EA-2" ~ "EA-2",
      x == "EAST-AFRICA-3-EA-3" ~ "EA-3",
      x == "EAST-AFRICA-4-EA-4" ~ "EA-4",
      x == "I-NORTHWEST-ZIMBABWE-NWZ" ~ "NWZ",
      x == "I-SOUTHEAST-ZIMBABWE-SEZ" ~ "SEZ",
      x == "III-NORTHWEST-ZIMBABWE-NWZ" ~ "NWZ",
      x == "II-WESTERN-ZIMBABWE-WZ" ~ "WZ",
      x == "III-WESTERN-ZIMBABWE-WZ" ~ "WZ",
      x == "INDONESIA-1-ISA-1-1" ~ "ISA-1",
      x == "IV-EAST-AFRICA1-EA-1" ~ "EA-1",
      x == "MIDDLE-EAST-SOUTH-ASIA-ME-SA" ~ "ME-SA",
      x == "V-East Africa-EA" ~ "V-EA",
      x == "VII-EAST-AFRICA-2-EA-2" ~ "VII-EA-2",
      x == "WEST-AFRICA-WA" ~ "WA",
      TRUE ~ x
    )
  })
  
  # Подготовка данных для heatbars
  heat_data = data.frame(
    "serotype" = info$serotype,
    "Topotype" = info$Topotype
  )
  rownames(heat_data) <- info$GBAC
  
  # Построение дерева с градиентной окраской
  t = ggtree(tree_rooted, size=0.1) %<+% info + 
    geom_nodepoint(aes(label = label, 
                       subset = !is.na(as.numeric(label)) & as.numeric(label) >= 100),
                   size = 0.01, color = "green") +  
    geom_tiplab(size = 0.4, aes(color=label)) +
    scale_color_manual(values=info$color, guide='none') + 
    theme(legend.position = "none") 
  
  # Добавление heatbar для серотипов с новым scale fill
  t_with_serotype <- gheatmap(t, heat_data["serotype"], 
                              offset = 0.5, 
                              width = 0.1, 
                              color = NULL,
                              colnames=FALSE) +
    scale_fill_manual(values=serotype_colors, name = "Serotype")
  
  # Добавление нового scale fill перед topotype heatmap
  t_with_serotype <- t_with_serotype + ggnewscale::new_scale_fill()
  
  # Добавление heatbar для топотипов с abbreviated names
  t_with_both <- gheatmap(t_with_serotype, heat_data["Topotype"],
                          offset = 0.7,
                          width = 0.1,
                          color = NULL,
                          colnames=FALSE,
                          legend_title='Topotype') 
    #scale_fill_manual(values=topotype_colors_abbreviated, name = "Topotype") +
    #theme(legend.position = "right")
  
  return(t_with_both)
}



# Построение и сохранение деревьев
 for (file in trees) {
   g = plot_tree_with_gradient_and_heatmap(file, meta_path, serotype_colors, topotype_colors) +
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
       legend.text = element_text(size = 6),
       legend.title = element_text(size = 8)
       #legend.spacing.y = unit(0.2, "cm")
     )
   g
   
   png_file <- paste0("Images/HeatbarAndGradient/", basename(file), "_combined.png")
   svg_file <- paste0("Images/HeatbarAndGradient/", basename(file), "_combined.svg")
   
   ggsave(png_file, g, height = 10, width = 7, dpi = 600)
   ggsave(svg_file, g, height = 10, width = 7, dpi = 600)
 }

