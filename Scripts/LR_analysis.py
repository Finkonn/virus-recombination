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

    # Create the figure and grid
    fig = plt.figure(figsize=(16, 20))
    grid = fig.add_gridspec(nrows=5, ncols=2, height_ratios=[2, 1, 1, 1, 1])
    ax_main = fig.add_subplot(grid[0, :])
    
    # Main scatter plot
    sns.scatterplot(data=region_data, x='date', y='distance', ax=ax_main, color='blue')
    ax_main.set_title(f'Root-to-tip distances versus sampling time of {region} region', fontsize=16)

    X_main = region_data['date'].values.reshape(-1, 1)
    y_main = region_data['distance'].values

    # Calculations
    corr_coeff, p_corr = pearsonr(region_data['date'], region_data['distance'])

    spearman_corr, p_spearman = spearmanr(region_data['date'], region_data['distance'])

    lin_regression_pvalue = linregress(region_data['date'], region_data['distance'])
    lin_regression_pvalue = lin_regression_pvalue.pvalue

    model_main = LinearRegression()
    model_main.fit(X_main, y_main)
    y_main_pred = model_main.predict(X_main)
    r_squared_main = r2_score(y_main, y_main_pred)

    # Main label
    main_metrics_label = (f'Pearson r: {corr_coeff:.2f}\n'
                        f'p-value: {p_corr:.2e}\n\n'
                        f'Spearman r: {spearman_corr:.2f}\n'
                        f'pvalue: {p_spearman:.2e}\n\n'
                        f'p-value (LR): {lin_regression_pvalue:.2e}\n'
                        f'R²: {r_squared_main:.2f}')

    sns.regplot(data=region_data, x='date', y='distance', scatter=False, 
                ax=ax_main, color='red', label=main_metrics_label)
    ax_main.legend()

    # Subplots for each serotype
    for i, serotype in enumerate(serotypes):
        row = (i // 2) + 1
        col = i % 2
        ax = fig.add_subplot(grid[row, col])

        serotype_data = data[data['serotype'] == serotype]
        sns.scatterplot(data=serotype_data, x='date', y='distance', ax=ax, color='blue')
        ax.set_title(f'Serotype: {serotype}')

        # Calculations
        corr_coeff, p_corr = pearsonr(serotype_data['date'], serotype_data['distance'])

        spearman_corr, p_spearman = spearmanr(serotype_data['date'], serotype_data['distance'])

        lin_regression_pvalue = linregress(serotype_data['date'], serotype_data['distance'])
        lin_regression_pvalue = lin_regression_pvalue.pvalue

        # Linear regression for serotype + r2
        X = serotype_data['date'].values.reshape(-1, 1)
        y = serotype_data['distance'].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r_squared = r2_score(y, y_pred)

        # Serotype label
        metrics_label = (f'Pearson r: {corr_coeff:.2f}\n'
                         f'p-value: {p_corr:.2e}\n\n'
                         f'Spearman r: {spearman_corr:.2f}\n'
                         f'pvalue: {p_spearman:.2e}\n\n'
                         f'p-value (LR): {lin_regression_pvalue:.2e}\n'
                         f'R²: {r_squared:.2f}')

        sns.regplot(data=serotype_data, x='date', y='distance', scatter=False, ax=ax, color='red', label=metrics_label)
        ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left') 

    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    png_filename = os.path.join(output_path, f"{region}_temporal_signal_plot.png")
    svg_filename = os.path.join(output_path, f"{region}_temporal_signal_plot.svg")
    plt.savefig(png_filename, format='png')
    plt.savefig(svg_filename, format='svg')

    #plt.show()

