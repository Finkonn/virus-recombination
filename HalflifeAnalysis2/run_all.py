import os
import subprocess
import shutil
import pandas as pd

mcc_dir = "MCC"
regions = ["Lpro", "P1", "P2", "P3"]
serotypes = ["A", "O", "Asia1", "SAT1", "SAT2", "SAT3", "C"]
results_dir = "Results"
script = "get_RF_halflife.py"

os.makedirs(results_dir, exist_ok=True)

for filename in os.listdir(mcc_dir):
    if not filename.endswith(".tree"):
        continue

    tree1_path = os.path.join(mcc_dir, filename)
    parts = filename.replace(".tree", "").split("_")
    if len(parts) != 2:
        print(f"Пропущен файл: {filename}")
        continue
    serotype, _ = parts

    sero_outdir = os.path.join(results_dir, serotype)
    os.makedirs(sero_outdir, exist_ok=True)

    for region in regions:
        tree2_path = os.path.join(region, f"{serotype}.treefile")

        if not os.path.exists(tree2_path):
            print(f"Пропущен: {tree2_path} (не найден)")
            continue

        print(f"Анализ: {filename} с {tree2_path}")

        subprocess.run([
            "python", script,
            "-tree1", tree1_path,
            "-tree2", tree2_path,
            "-method", "all",
            "-thr", "0.8",
            "-thr2", "0.8"
        ])

        base1 = os.path.basename(tree1_path).replace(".tree", "")
        base2 = os.path.basename(tree2_path).replace(".treefile", "")
        common_prefix = f"{base1}_{base2}"

        for f in os.listdir("."):
            if f.startswith(common_prefix):
                ext = f[len(common_prefix):]  
                new_name = f"{serotype}_{region}{ext}"
                shutil.move(f, os.path.join(sero_outdir, new_name))
                print(f"    -> {new_name} сохранён")

combined = []
for serotype in serotypes:
    sero_dir = os.path.join(results_dir, serotype)
    if not os.path.isdir(sero_dir):
        continue
    for file in os.listdir(sero_dir):
        if file.endswith("_table.csv"):
            path = os.path.join(sero_dir, file)
            df = pd.read_csv(path)
            
            name_parts = file.replace("_table.csv", "").split("_")
            if len(name_parts) == 2:
                df.insert(0, "serotype", name_parts[0])
                df.insert(1, "region", name_parts[1])
                combined.append(df)

if combined:
    merged_df = pd.concat(combined, ignore_index=True)
    merged_df.to_csv(os.path.join(results_dir, "All_RF_tables.csv"), index=False)
    print("\nОбъединённая таблица сохранена в Results/All_RF_tables.csv")
else:
    print("\nНет таблиц для объединения.")

print("\nГотово. Все результаты в папке Results.")
