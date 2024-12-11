import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

main_path = "../RegressionData/"
output_path = "../RegressionData/Images"
os.makedirs(output_path, exist_ok=True)

regions = ['P1', 'P2', 'P3', 'VP1', 'Lpro']

for region in regions:
    region_path = os.path.join(main_path, region)
    all_files = [file for file in os.listdir(region_path) if file.endswith('.csv')]

    region_file = os.path.join(region_path, f"{region}.csv")
    region_data = pd.read_csv(region_file, sep='\t')
    serotype_files = [file for file in all_files if file != f"{region}.csv"]

    data_list = []
    for file in serotype_files:
        df = pd.read_csv(os.path.join(region_path, file), sep='\t')
        df['serotype'] = os.path.basename(file).replace('.csv', '') 
        data_list.append(df)
    
    data = pd.concat(data_list, ignore_index=True)
    serotypes = data['serotype'].unique()

    # Создаем фигуру и оси
    fig = plt.figure(figsize=(16, 20))
    grid = fig.add_gridspec(nrows=5, ncols=2, height_ratios=[2, 1, 1, 1, 1])  
    ax_main = fig.add_subplot(grid[0, :])
    sns.scatterplot(data=region_data, x='date', y='distance', ax=ax_main, color='blue')
    ax_main.set_title(f'Root-to-tip distances versus sampling time of {region} region (Main Graph)', fontsize=16)

    # Линейная регрессия и расчет R^2 для региона
    X_main = region_data['date'].values.reshape(-1, 1)
    y_main = region_data['distance'].values
    model_main = LinearRegression()
    model_main.fit(X_main, y_main)
    y_main_pred = model_main.predict(X_main)
    r_squared_main = r2_score(y_main, y_main_pred)

    metrics_label_main = f'Region R²: {r_squared_main:.2f}'
    sns.regplot(data=region_data, x='date', y='distance', scatter=False, ax=ax_main, color='red', label=metrics_label_main)
    ax_main.legend()

    # Подграфики для каждого серотипа
    for i, serotype in enumerate(serotypes):
        row = (i // 2) + 1  
        col = i % 2
        ax = fig.add_subplot(grid[row, col])

        serotype_data = data[data['serotype'] == serotype]
        sns.scatterplot(data=serotype_data, x='date', y='distance', ax=ax, color='blue')
        ax.set_title(f'Serotype: {serotype}')

        # Корреляция и линейная регрессия
        corr_coeff, _ = pearsonr(serotype_data['date'], serotype_data['distance'])
        X = serotype_data['date'].values.reshape(-1, 1)
        y = serotype_data['distance'].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r_squared = r2_score(y, y_pred)

        # Добавляем подписи
        metrics_label = f'Correlation: {corr_coeff:.2f}\nR²: {r_squared:.2f}'
        sns.regplot(data=serotype_data, x='date', y='distance', scatter=False, ax=ax, color='red', label=metrics_label)
        ax.legend()

    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Сохранение графиков
    png_filename = os.path.join(output_path, f"{region}_temporal_signal_plot.png")
    svg_filename = os.path.join(output_path, f"{region}_temporal_signal_plot.svg")
    plt.savefig(png_filename, format='png')
    plt.savefig(svg_filename, format='svg')

    plt.show()
