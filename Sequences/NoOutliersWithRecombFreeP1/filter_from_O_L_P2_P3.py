from Bio import SeqIO

# Путь к исходному файлу с нужными ID
reference_file = "O.fastaO_random_1_10.0_0.fasta"

# Целевые файлы, которые нужно отфильтровать
target_files = ["O_L.fasta", "O_P2.fasta", "O_P3.fasta"]

# Чтение ID из референсного файла
reference_ids = set(rec.id for rec in SeqIO.parse(reference_file, "fasta"))

print(f"[INFO] Найдено {len(reference_ids)} ID в {reference_file}")

# Фильтрация каждого файла
for target_file in target_files:
    records = SeqIO.parse(target_file, "fasta")
    filtered = [rec for rec in records if rec.id in reference_ids]
    
    output_file = f"filtered_{target_file}"  # можно заменить на нужную папку
    SeqIO.write(filtered, output_file, "fasta")
    
    print(f"[DONE] {target_file} → {output_file} | Сохранено: {len(filtered)} последовательностей")
