from Bio import SeqIO
import os

# Пути к папкам
filter_dir = "P1"
target_dir = "P3"
output_dir = "filtered_output"

# Создаём выходную папку
os.makedirs(output_dir, exist_ok=True)

# Обрабатываем каждый файл из filter_dir
for filename in os.listdir(filter_dir):
    if filename.endswith(".fasta"):
        filter_path = os.path.join(filter_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        if not os.path.exists(target_path):
            print(f"[!] Пропущен файл (нет соответствия во второй папке): {filename}")
            continue

        # Читаем ID из filter файла
        filter_ids = set(rec.id for rec in SeqIO.parse(filter_path, "fasta"))
        
        # Фильтруем целевой файл
        filtered_records = [
            rec for rec in SeqIO.parse(target_path, "fasta") if rec.id in filter_ids
        ]
        
        # Сохраняем результат
        output_path = os.path.join(output_dir, filename)
        SeqIO.write(filtered_records, output_path, "fasta")
        print(f"[+] Отфильтровано {len(filtered_records)} последовательностей: {filename}")
