import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress, pearsonr, spearmanr

df = pd.read_excel('meta_no_probang_removed_seqs.xlsx')

all_correlation_results = []

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
        
        data['accession'] = data['tip'].apply(lambda x: x.split('/')[0] if isinstance(x, str) else x)
        data['in_meta_table'] = data['accession'].isin(df['Genbank accession'])
        
        data_in_meta = data[data['in_meta_table']]
        data_not_in_meta = data[~data['in_meta_table']]
        
        if not data_not_in_meta.empty:
            sns.scatterplot(data=data_not_in_meta, x='date', y='distance', 
                           color='blue', ax=ax, size=1)
        
        if not data_in_meta.empty:
            sns.scatterplot(data=data_in_meta, x='date', y='distance', 
                           color='red', ax=ax, size=1)
        
        X = data['date'].values.reshape(-1, 1)
        y = data['distance'].values
        
        slope, intercept, r_value, linreg_pvalue, std_err = linregress(data['date'], data['distance'])
        r_squared = r_value ** 2
        
        pearson_corr, pearson_p = pearsonr(data['date'], data['distance'])
        spearman_corr, spearman_p = spearmanr(data['date'], data['distance'])
        
        model = LinearRegression()
        model.fit(X, y)

        intercept_str = f"- {abs(intercept):.2f}" if intercept < 0 else f"+ {intercept:.2f}"

        metrics_label = (f'Pearson r: {pearson_corr:.2f}\n'
                         f'p-value: {pearson_p:.2e}\n'
                         f'Spearman r: {spearman_corr:.2f}\n'
                         f'p-value: {spearman_p:.2e}\n'
                         f'Linear regression:\n'
                         f'y = {slope:.2e}x {intercept_str}\n'
                         f'p-value: {linreg_pvalue:.2e}\n'
                         f'R²: {r_squared:.2f}'
                         )

        result = {
            'serotype': serotype,
            'file': file.split('.')[0],
            'pearson_corr': pearson_corr,
            'pearson_p': pearson_p,
            'spearman_corr': spearman_corr,
            'spearman_p': spearman_p,
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'linreg_pvalue': linreg_pvalue,
        }
        all_correlation_results.append(result)

        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_range = model.predict(x_range)
        ax.plot(x_range, y_range, color='red', linewidth=1, label='Linear regression')
        
        ax.set_title(f"{file.split('.')[0]}", fontsize=10)
        ax.set_xlabel("Collection year", fontsize=9)
        ax.set_ylabel("Root-to-tip distance", fontsize=9)
        ax.tick_params(labelsize=7)
        
        ax.legend([metrics_label], fontsize=7, handlelength=0)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_file_png = os.path.join(output_path, serotype + "_graph_LR_no_probang.png")
    output_file_svg = os.path.join(output_path, serotype + "_graph_LR_no_probang.svg")
    plt.savefig(output_file_png, format='png')
    plt.savefig(output_file_svg, format='svg')
    plt.close()
    
    for file in csv_files:
        file_path = os.path.join(main_path, file)
        data = pd.read_csv(file_path, sep='\t')
        data['accession'] = data['tip'].apply(lambda x: x.split('/')[0] if isinstance(x, str) else x)
        data['in_meta_table'] = data['accession'].isin(df['Genbank accession'])
        
        total_points = len(data)
        red_points = data['in_meta_table'].sum()
        
        print(f"  {file}: {red_points}/{total_points} points in meta table")

correlation_df = pd.DataFrame(all_correlation_results)

# Функция для форматирования чисел
def format_number(x):
    """Форматирует число: 
       - если экспонента >= -1 (т.е. e-01, e-00 и т.д.), то в обычном формате с 2 знаками
       - иначе в научной нотации с 2 знаками"""
    try:
        if pd.isnull(x):
            return x
        
        # Преобразуем в строку в научной нотации
        str_e = f"{x:.2e}"
        
        # Извлекаем экспоненту
        if 'e' in str_e:
            base, exp_str = str_e.split('e')
            exp = int(exp_str)
            
            # Если экспонента >= -1 (т.е. e-01, e-00, e+...), используем обычный формат
            if exp >= -1:
                return f"{x:.2f}"
            else:
                # Для очень маленьких чисел оставляем научную нотацию
                return str_e
        else:
            # Если нет 'e', значит это обычное число
            return f"{x:.2f}"
    except:
        return str(x)

# Создаем отформатированный DataFrame
formatted_df = correlation_df.copy()

# Применяем форматирование только к числовым столбцам
numeric_cols = ['pearson_corr', 'pearson_p', 'spearman_corr', 'spearman_p', 
                'slope', 'intercept', 'r_squared', 'linreg_pvalue']

for col in numeric_cols:
    if col in formatted_df.columns:
        formatted_df[col] = formatted_df[col].apply(format_number)

# Сохраняем отформатированный DataFrame
correlation_csv = "correlation_coefficients_new_data.csv"
formatted_df.to_csv(correlation_csv, index=False)

print(f"Результаты сохранены в файл: {correlation_csv}")
print(f"Количество записей: {len(correlation_df)}")