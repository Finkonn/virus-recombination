import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Пути
main_path = "../Random_sampling/O_random_samples"
output_path = os.path.join(main_path, "output")
os.makedirs(output_path, exist_ok=True)

# Получаем список всех CSV файлов
csv_files = [f for f in os.listdir(main_path) if f.endswith('.csv')]

# Определяем размер полотна
fig, axes = plt.subplots(nrows=len(csv_files), ncols=1, figsize=(10, 5 * len(csv_files)))
fig.suptitle("Graphs for CSV Files", fontsize=16)

if len(csv_files) == 1:
    axes = [axes]

for ax, file in zip(axes, csv_files):
    file_path = os.path.join(main_path, file)
    data = pd.read_csv(file_path, sep='\t')
    
    sns.scatterplot(data=data, x='date', y='distance', color='blue', ax=ax)
    sns.regplot(data=data, x='date', y='distance', scatter=False, color='red', ax=ax)
    
    ax.set_title(f"Graph for {file}", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Distance")

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_file_png = os.path.join(output_path, "all_graphs.png")
output_file_svg = os.path.join(output_path, "all_graphs.svg")
plt.savefig(output_file_png, format='png')
plt.savefig(output_file_svg, format='svg')
plt.close()
