import re

# Функция для обработки Nexus файла
def process_nexus_file(input_file, output_file):
    reference_colors = {}  # Словарь для хранения цветов референсов и их топотипов
    sequences = []  # Список для хранения всех последовательностей

    # Регулярное выражение для извлечения цвета
    color_pattern = re.compile(r"\[&!color=(?P<color>#\w+)\]")

    # Чтение Nexus файла
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Удаляем лишние пробелы
            if not line or ";" in line:  # Пропускаем пустые строки или строки после `;`
                continue

            # Разделяем строку по нижнему подчеркиванию
            parts = line.split("_")
            if len(parts) < 2:
                continue

            # Извлекаем данные
            name = parts[0]
            second_part = parts[1]
            last_part = parts[-1]

            # Проверяем, является ли строка референсом
            if second_part in {"O", "A", "Asia1", "SAT1", "SAT2", "SAT3", "C"}:
                # Это референс, сохраняем топотип и цвет
                topotype = last_part.split("[")[0]  # Убираем все после "[", если есть
                match = color_pattern.search(line)
                if match:
                    color = match.group("color")
                    reference_colors[color] = topotype
            else:
                # Это обычная последовательность
                match = color_pattern.search(line)
                if match:
                    color = match.group("color")
                    sequences.append((line, color))  # Сохраняем всю строку и её цвет

    # Создание выходных данных
    with open(output_file, 'w') as file:
        for seq, color in sequences:
            if color in reference_colors:
                topotype = reference_colors[color]
                # Удаляем цвет из строки
                cleaned_seq = re.sub(r"\[&!color=#\w+\]", "", seq)
                file.write(f"{cleaned_seq}_{topotype}\n")

# Пример вызова функции
input_nexus_file = "../Trees/VP1_topotype_colored.nexus"  # Входной Nexus файл
output_file = "../Maps/genotyped_topotypes.txt"  # Выходной файл
process_nexus_file(input_nexus_file, output_file)
