import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr, spearmanr, linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

main_path = "RandomSamplingTemp/O_single_picking/tempest_data"
output_path = os.path.join(main_path)
os.makedirs(output_path, exist_ok=True)

csv_files = [f for f in os.listdir(main_path) if f.endswith('.csv')]

fig, axes = plt.subplots(nrows=len(csv_files), ncols=1, figsize=(10, 5 * len(csv_files)))
if len(csv_files) == 1:
    axes = [axes]

for ax, file in zip(axes, csv_files):
    file_path = os.path.join(main_path, file)
    data = pd.read_csv(file_path, sep='\t')

    sns.scatterplot(data=data, x='date', y='distance', color='blue', ax=ax)

    X = data['date'].values.reshape(-1, 1)
    y = data['distance'].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r_squared = r2_score(y, y_pred)

    corr_coeff, p_corr = pearsonr(data['date'], data['distance'])
    spearman_corr, p_spearman = spearmanr(data['date'], data['distance'])
    lin_reg_pval = linregress(data['date'], data['distance']).pvalue

    slope = model.coef_[0]
    intercept = model.intercept_

    intercept_str = f"- {abs(intercept):.2f}" if intercept < 0 else f"+ {intercept:.2f}"

    metrics_label = (f'Коэфф. Спирмена: {spearman_corr:.2f}\n'
                     f'p-value: {p_spearman:.2e}\n'
                     f'y = {slope:.4f}x {intercept_str}')



    sns.regplot(data=data, x='date', y='distance', scatter=False, color='red', ax=ax)

    ax.set_title(f"{file.split('.')[0]}", fontsize=24)
    ax.set_xlabel("Год", fontsize=20)
    ax.set_ylabel("Генетическое расстояние", fontsize=20)
    ax.tick_params(labelsize=16)
    ax.legend(fontsize=14)

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_file_png = os.path.join(output_path, "all_graphs.png")
output_file_svg = os.path.join(output_path, "all_graphs.svg")
plt.savefig(output_file_png, format='png')
plt.savefig(output_file_svg, format='svg')
plt.close()
