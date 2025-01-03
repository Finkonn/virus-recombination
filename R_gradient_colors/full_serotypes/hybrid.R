library('ggtree')
library('ggplot2')
library('phytools')
library('dplyr')

setwd("C:/Users/Mate_/Downloads/Diploma/virus-recombination/R_gradient_colors/full_serotypes")

source("../modified_gradients.R")

# Список файлов с деревьями
trees = list.files(path = ".", full.names = TRUE, pattern = ".treefile$")
meta_path = "metadata_upd_full.csv"


# Цвета для серотипов
info = read.csv(meta_path)
unique_serotypes <- unique(info$serotype)
serotype_colors <- setNames(c("#B7B718", "#B67603", "#5F93B3", "#BDB9DB", "#D54514", "#3F9588", "#9FC845"), 
                            unique_serotypes)

# Функция для построения дерева с градиентами и heatbar
plot_tree_with_gradient_and_heatmap = function(tree_file, meta, serotype_colors) {
  # Загрузка и корневание дерева
  tree = read.tree(tree_file)
  tree_rooted = midpoint.root(tree)
  
  # Загрузка метаданных
  info = read.csv(meta)
  
  # Подготовка данных для heatbar
  serotypes = data.frame("serotypes" = info$serotype)
  rownames(serotypes) <- info$GBAC
  
  # Построение дерева с градиентной окраской
  t = ggtree(tree_rooted, size=0.1) %<+% info + 
    geom_text2(aes(label = label, 
                   subset = !is.na(as.numeric(label)) & as.numeric(label) >= 80),
               size = 1, color = "black") +  
    
    geom_tiplab(size = 2, aes(color=label)) +
    
    scale_color_manual(values=info$color, guide='none') + 
    theme(legend.position = "none") +
    xlim_expand(1, panel = 'label')
  
  # Добавление heatbar
  t_with_heatmap = gheatmap(t, serotypes, 
                            offset = 0.7, 
                            width = 0.1, 
                            colnames_position = "top", 
                            colnames_angle = 0, 
                            colnames_offset_y = 20, 
                            color = NULL) +
    scale_fill_manual(values=serotype_colors, name = "Serotype")
  
  return(t_with_heatmap)
}

# Построение и сохранение деревьев
for (file in trees) {
  # Построение дерева с градиентами и heatbar
  g = plot_tree_with_gradient_and_heatmap(file, meta_path, serotype_colors) +
    ggtitle(strsplit(basename(file), '.treefile')[[1]][1])
  
  # Сохранение результатов
  png_file <- paste0("Images/HeatbarAndGradient/", basename(file), "_combined.png")
  svg_file <- paste0("Images/HeatbarAndGradient/", basename(file), "_combined.svg")
  
  ggsave(png_file, g, height = 10, width = 7, dpi = 600)
  ggsave(svg_file, g, height = 10, width = 7, dpi = 300)
}

