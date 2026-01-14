import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats  
from scipy.stats import linregress, pearsonr, spearmanr

for serotype in ['A', 'Asia1', 'O', 'C', 'SAT1', 'SAT2', 'SAT3']:

    main_path = os.path.join(serotype)
    output_path = os.path.join(serotype)

    os.makedirs(output_path, exist_ok=True)

    csv_files = [f for f in os.listdir(main_path) if f.endswith('.csv')]

    fig, axes = plt.subplots(nrows=len(csv_files), ncols=1, figsize=(4, 2.5 * len(csv_files)))
    if len(csv_files) == 1:
        axes = [axes]

    for ax, file in zip(axes, csv_files):
        file_path = os.path.join(main_path, file)
        data = pd.read_csv(file_path, sep='\t')

        sns.scatterplot(data=data, x='date', y='distance', color='blue', ax=ax, size=1)

        X = data['date'].values.reshape(-1, 1)
        y = data['distance'].values
        
        slope, intercept, r_value, linreg_pvalue, std_err = linregress(data['date'], data['distance'])
        r_squared = r_value ** 2
        
        pearson_corr, pearson_p = pearsonr(data['date'], data['distance'])
        spearman_corr, spearman_p = spearmanr(data['date'], data['distance'])
        
        model = LinearRegression()
        model.fit(X, y)

        intercept_str = f"- {abs(intercept):.2f}" if intercept < 0 else f"+ {intercept:.2f}"

        metrics_label = (#f'Pearson r: {pearson_corr:.2f}\n'
                         #f'p-value: {pearson_p:.2e}\n'
                         f'Spearman r: {spearman_corr:.2f}\n'
                         f'p-value: {spearman_p:.2e}\n'
                         #f'Linear regression:\n'
                         f'y = {slope:.2e}x {intercept_str}\n'
                         f'p-value: {linreg_pvalue:.2e}\n'
                         #f'R²: {r_squared:.2f}'
                         )

        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_range = model.predict(x_range)
        ax.plot(x_range, y_range, color='red', linewidth=1, label='Linear regression')
        
        ax.set_title(f"{file.split('.')[0]}", fontsize=10)
        ax.set_xlabel("Collection year", fontsize=9)
        ax.set_ylabel("Root-to-tip distance", fontsize=9)
        ax.tick_params(labelsize=7)
        ax.legend([metrics_label], fontsize=7, handlelength=0)  

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_file_png = os.path.join(output_path,serotype+"_graph_LR_bigger.png")
    output_file_svg = os.path.join(output_path,serotype+"_graph_LR_bigger.svg")
    plt.savefig(output_file_png, format='png')
    plt.savefig(output_file_svg, format='svg')
    plt.close()