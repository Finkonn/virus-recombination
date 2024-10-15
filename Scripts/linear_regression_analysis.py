import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

main_path = "../RegressionData/"
regions = ['P1', 'P2', 'P3', 'VP1']

for region in regions:
    region_path = os.path.join(main_path, region)
    all_files = [file for file in os.listdir(region_path) if file.endswith('.csv')]

    data_list = []
    
    for file in all_files:
        df = pd.read_csv(os.path.join(region_path, file), sep='\t')
        df['serotype'] = os.path.basename(file).replace('.csv', '')  # Извлекаем серотип из имени файла
        data_list.append(df)
    
    # Объединяем все данные участка в один DataFrame
    data = pd.concat(data_list, ignore_index=True)
    serotypes = data['serotype'].unique()
    
    # Создаем подграфики для каждого серотипа
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(16, 16))
    fig.suptitle(f'Root-to-tip distances versus sampling time of {region} region', fontsize=16)
    axes = axes.flatten()
    
    for i, serotype in enumerate(serotypes):
        ax = axes[i]
        # Фильтруем данные для текущего серотипа
        serotype_data = data[data['serotype'] == serotype]

        sns.scatterplot(data=serotype_data, x='date', y='distance', ax=ax, color='blue')
        
        if serotype in ['P1', 'P2', 'P3', 'VP1']:
            ax.set_title(f'Region: {serotype}')
        else:
            ax.set_title(f'Serotype: {serotype}')

        # Рассчитываем корреляцию
        corr_coeff, _ = pearsonr(serotype_data['date'], serotype_data['distance'])

        # Линейная регрессия и расчет R^2
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
        ax.set_xlabel('')

    plt.subplots_adjust(wspace=0.086, hspace=0.340)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()
