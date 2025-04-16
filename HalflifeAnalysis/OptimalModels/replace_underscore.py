import os
import glob

folders = ["Lpro", "P1", "P2", "P3"]

for folder in folders:
    treefiles = glob.glob(os.path.join(folder, "*.treefile"))

    for filepath in treefiles:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Заменяем "_" на "/"
        modified_content = content.replace("_", "/")

        # Сохраняем обратно
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified_content)

        print(f"Обработан файл: {filepath}")
