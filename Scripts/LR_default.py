import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr, spearmanr, linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Пути
main_path = "../RandomSampling/O_random_samples"
output_path = os.path.join(main_path, "regression_graph")
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
    
    # Линейная регрессия
    X = data['date'].values.reshape(-1, 1)
    y = data['distance'].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r_squared = r2_score(y, y_pred)
    
    # Корреляции
    corr_coeff, p_corr = pearsonr(data['date'], data['distance'])
    spearman_corr, p_spearman = spearmanr(data['date'], data['distance'])
    lin_reg_pval = linregress(data['date'], data['distance']).pvalue
    
    # Метки с метриками
    metrics_label = (f'Pearson r: {corr_coeff:.2f}\n'
                     f'p-value: {p_corr:.2e}\n\n'
                     f'Spearman r: {spearman_corr:.2f}\n'
                     f'p-value: {p_spearman:.2e}\n\n'
                     f'p-value (LR): {lin_reg_pval:.2e}\n'
                     f'R²: {r_squared:.2f}')
    
    sns.regplot(data=data, x='date', y='distance', scatter=False, color='red', ax=ax, label=metrics_label)
    
    ax.set_title(f"Graph for {file}", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Distance")
    ax.legend(fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_file_png = os.path.join(output_path, "all_graphs.png")
output_file_svg = os.path.join(output_path, "all_graphs.svg")
plt.savefig(output_file_png, format='png')
plt.savefig(output_file_svg, format='svg')
plt.close()
