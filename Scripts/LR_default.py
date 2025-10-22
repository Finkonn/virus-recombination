import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats  # Only for p-value calculation

main_path = "../RegressionData/RecombinationFree"
output_path = "../Plots/RegressionAnalysis/RecombFree"

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
    
    # Use only LinearRegression for all calculations
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    # Calculate metrics using the model
    r_squared = r2_score(y, y_pred)
    slope = model.coef_[0]
    intercept = model.intercept_
    
    # Calculate p-value for the regression manually
    n = len(y)
    dof = n - 2  # degrees of freedom
    t_statistic = (slope) / np.sqrt(np.sum((y - y_pred)**2) / dof / np.sum((X - np.mean(X))**2))
    p_value = 2 * (1 - stats.t.cdf(np.abs(t_statistic), dof))
    
    # Calculate Spearman correlation separately (not part of linear regression)
    spearman_corr = stats.spearmanr(data['date'], data['distance']).correlation
    
    intercept_str = f"- {abs(intercept):.2f}" if intercept < 0 else f"+ {intercept:.2f}"

    metrics_label = (f'Spearman coeff.: {spearman_corr:.2f}\n'
                     f'p-value: {p_value:.2e}\n'
                     f'y = {slope:.4f}x {intercept_str}\n'
                     f'R²: {r_squared:.2f}')

    # Plot regression line using the model predictions
    x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_range = model.predict(x_range)
    ax.plot(x_range, y_range, color='red', linewidth=2, label='Linear regression')
    
    # Alternative: you could also use the slope and intercept directly:
    # ax.plot(x_range, intercept + slope * x_range, color='red', linewidth=2)

    ax.set_title(f"{file.split('.')[0]}", fontsize=24)
    ax.set_xlabel("Year", fontsize=20)
    ax.set_ylabel("Genetic distance", fontsize=20)
    ax.tick_params(labelsize=16)
    ax.legend([metrics_label], fontsize=14, handlelength=0)  # Remove the line from legend

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_file_png = os.path.join(output_path, "SAT3_graphs.png")
output_file_svg = os.path.join(output_path, "SAT3_graphs.svg")
plt.savefig(output_file_png, format='png')
plt.savefig(output_file_svg, format='svg')
plt.close()