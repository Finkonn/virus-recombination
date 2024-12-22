import pandas as pd
import os
import argparse

# Функция для обработки каждого CSV файла
def process_file(file_path):
    # Чтение файла с табуляцией
    df = pd.read_csv(file_path, sep='\t', header=None)
    # Разделяем строки на несколько столбцов по символу табуляции
    df = df[0].str.split('\t', expand=True)
    # Переименовываем столбцы
    df.columns = ['tip', 'date', 'distance', 'residual']
    # Удаляем первую строку
    df = df.iloc[1:].reset_index(drop=True)
    return df

# Функция для конвертации столбцов в нужный формат
def save_with_float_columns(df, output_file):
    # Преобразуем столбцы 'date', 'distance', 'residual' в тип float64
    df['date'] = df['date'].astype('float64')
    df['distance'] = df['distance'].astype('float64')
    df['residual'] = df['residual'].astype('float64')
    # Сохраняем в новый файл
    df.to_csv(output_file, index=False, sep='\t')

def main(input_dir, output_file_name):
    # Проверка, что директория существует
    if not os.path.isdir(input_dir):
        print(f"Ошибка: Директория {input_dir} не существует.")
        return
    
    # Путь к главному файлу
    main_file_path = os.path.join(input_dir, output_file_name)
    
    # Проверка, что главный файл существует
    if not os.path.isfile(main_file_path):
        print(f"Ошибка: Главный файл {main_file_path} не найден.")
        return

    # Чтение главного файла Lpro.csv
    lpro_df = process_file(main_file_path)

    # Список других файлов для обработки
    other_files = [
        'A.csv', 'Asia1.csv', 'C.csv', 'O.csv', 'SAT1.csv', 'SAT2.csv', 'SAT3.csv'
    ]

    # Список для хранения обработанных DataFrame
    other_dfs = []

    # Обработка всех остальных файлов
    for file in other_files:
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            df = process_file(file_path)
            other_dfs.append(df)
        else:
            print(f"Предупреждение: Файл {file_path} не найден. Он будет пропущен.")

    # Если нет других файлов для обработки
    if not other_dfs:
        print("Ошибка: Нет доступных других файлов для обработки.")
        return

    # Объединяем все другие файлы в один DataFrame
    combined_df = pd.concat(other_dfs, ignore_index=True)

    # Убираем дубликаты в объединенных данных
    combined_df = combined_df.drop_duplicates()

    # Мержим Lpro с объединёнными данными по столбцу 'tip', чтобы оставить только те строки, которые есть в других файлах
    lpro_filtered = pd.merge(lpro_df, combined_df[['tip']], on='tip', how='inner')

    # Сохранение отфильтрованного файла
    lpro_filtered.to_csv(main_file_path, index=False, sep='\t')

    print(f"Файл '{output_file_name}' был перезаписан с {len(lpro_filtered)} строками.")

    # Обрабатываем и сохраняем все остальные файлы с правильными типами данных
    for file in other_files:
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            df = process_file(file_path)
            save_with_float_columns(df, file_path)  # Перезаписываем файл с новыми типами данных

    print("Все файлы были перезаписаны с правильными типами данных.")

if __name__ == "__main__":
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description="Обработка CSV файлов в указанной директории")
    parser.add_argument('input_dir', type=str, help="Путь к директории с файлами")
    parser.add_argument('output_file', type=str, help="Имя главного файла для перезаписи")

    args = parser.parse_args()

    # Запуск основной функции с аргументами
    main(args.input_dir, args.output_file)
