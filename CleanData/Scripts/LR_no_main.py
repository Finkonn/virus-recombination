import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr, spearmanr, linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

main_path = "../RegressionData/LessOutliers"
output_path = "../Plots/RegressionAnalysis/LessOutliers"
os.makedirs(output_path, exist_ok=True)

regions = ['Lpro', 'P1', 'P2', 'P3']

for region in regions:
    region_path = os.path.join(main_path, region)
    all_files = [file for file in os.listdir(region_path) if file.endswith('.csv')]

    region_file = os.path.join(region_path, f"{region}.csv")
    region_data = pd.read_csv(region_file, sep='\t')
    serotype_files = [file for file in all_files if file != f"{region}.csv"]

    # Collect data for each serotype
    data_list = []
    for file in serotype_files:
        df = pd.read_csv(os.path.join(region_path, file), sep='\t')
        df['serotype'] = os.path.basename(file).replace('.csv', '')
        data_list.append(df)
    
    data = pd.concat(data_list, ignore_index=True)
    serotypes = data['serotype'].unique()

    # Create the figure and grid (skip the main large subplot)
    fig = plt.figure(figsize=(14, 16))
    grid = fig.add_gridspec(nrows=4, ncols=2)

    for i, serotype in enumerate(serotypes):
        row = i // 2
        col = i % 2
        ax = fig.add_subplot(grid[row, col])

        serotype_data = data[data['serotype'] == serotype]
        sns.scatterplot(data=serotype_data, x='date', y='distance', ax=ax, color='blue')
        ax.set_title(f'Serotype: {serotype}')

        # Stats
        corr_coeff, p_corr = pearsonr(serotype_data['date'], serotype_data['distance'])
        spearman_corr, p_spearman = spearmanr(serotype_data['date'], serotype_data['distance'])
        linreg = linregress(serotype_data['date'], serotype_data['distance'])

        # Linear regression for line and R²
        X = serotype_data['date'].values.reshape(-1, 1)
        y = serotype_data['distance'].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r_squared = r2_score(y, y_pred)


        # Annotate inside the plot
        annotation = (
            f"Pearson r: {corr_coeff:.2f}, p={p_corr:.2e}\n"
            f"Spearman r: {spearman_corr:.2f}, p={p_spearman:.2e}\n"
            f"Linear Reg. p={linreg.pvalue:.2e}, R²={r_squared:.2f}"
        )
        # Red regression line
        sns.regplot(data=serotype_data, x='date', y='distance', scatter=False, ax=ax, color='red', label=annotation)

        ax.legend(fontsize=12)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    png_filename = os.path.join(output_path, f"no_main/{region}_no_main.png")
    svg_filename = os.path.join(output_path, f"no_main/{region}_no_main.svg")
    plt.savefig(png_filename, format='png')
    plt.savefig(svg_filename, format='svg')
    plt.close()
