import pandas as pd

# Загрузка входного текстового файла
with open("../Maps/genotyped_topotypes.txt", "r") as file:
    lines = file.read().strip().split("\n")

# Чтение файла с метаданными (CSV)
metadata = pd.read_csv("../R_gradient_colors/metadata.csv")

# Добавим столбец с первой частью идентификаторов (до первого '/')
metadata['GBAC_ID'] = metadata['GBAC'].apply(lambda x: x.split('/')[0])

# Функция для обработки каждой строки
def process_line(line):
    parts = line.split('_')
    gbac_id = parts[0]
    topotype = parts[-1]
    return gbac_id, topotype

# Список для хранения данных о найденных записях
processed_data = []

# Обрабатываем каждую строку из текстового файла
for line in lines:
    gbac_id, topotype = process_line(line)
    if gbac_id in metadata['GBAC_ID'].values:
        # Если ID найден, добавляем в список
        processed_data.append((gbac_id, topotype))

# Преобразуем в DataFrame для объединения
topotype_df = pd.DataFrame(processed_data, columns=['GBAC_ID', 'Topotype'])

# Объединяем по колонке GBAC_ID
result = metadata.merge(topotype_df, on='GBAC_ID', how='left')

# Удаляем временную колонку GBAC_ID, если она больше не нужна
result = result.drop(columns=['GBAC_ID'])

# Сохраняем результат в новый csv
result.to_csv("updated_metadata.csv", index=False)

print("Файл успешно обработан и сохранен как 'updated_metadata.csv'.")
