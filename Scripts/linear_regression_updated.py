import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import re

# Paths
main_path = "../RegressionData/RecombinationFree"
output_path = "../RegressionData/Images"
os.makedirs(output_path, exist_ok=True)
serotype_folders = [folder for folder in os.listdir(main_path) if os.path.isdir(os.path.join(main_path, folder))]

# Function to extract numeric coordinates from filenames
def extract_coordinates(filename):
    match = re.search(r'Coord_(\d+)_(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return float('inf'), float('inf')

for serotype in serotype_folders:
    serotype_path = os.path.join(main_path, serotype)
    all_files = sorted(
        [file for file in os.listdir(serotype_path) if file.endswith('.csv')],
        key=extract_coordinates
    )

    fig, axes = plt.subplots(nrows=len(all_files), ncols=1, figsize=(10, 5 * len(all_files)))
    fig.suptitle(f"Serotype: {serotype}", fontsize=20, y=0.97)  # Increased font size and adjusted position

    if len(all_files) == 1:
        axes = [axes]

    for i, file in enumerate(all_files):
        file_path = os.path.join(serotype_path, file)
        data = pd.read_csv(file_path, sep='\t')

        file_parts = file.replace('.csv', '').split('_')
        graph_name = f"{file_parts[-2]}-{file_parts[-1].split('.')[0]}"

        ax = axes[i]
        sns.scatterplot(data=data, x='date', y='distance', ax=ax, color='blue')
        ax.set_title(f"Graph for coordinates: {graph_name}", fontsize=14)  # Slightly increased font size

        X = data['date'].values.reshape(-1, 1)
        y = data['distance'].values
        corr_coeff, _ = pearsonr(data['date'], data['distance'])
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r_squared = r2_score(y, y_pred)

        sns.regplot(data=data, x='date', y='distance', scatter=False, ax=ax, color='red',
                    label=f"Correlation: {corr_coeff:.2f}\nR²: {r_squared:.2f}")
        ax.legend(fontsize=12)  # Slightly increased legend font size

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjusted layout for better spacing

    # Save plots for the current serotype
    png_filename = os.path.join(output_path, f"{serotype}_plots.png")
    svg_filename = os.path.join(output_path, f"{serotype}_plots.svg")
    plt.savefig(png_filename, format='png')
    plt.savefig(svg_filename, format='svg')
