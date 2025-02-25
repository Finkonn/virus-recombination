import os
import subprocess
import glob
from multiprocessing import Pool

folder = "O_single_picking"
exe = "iqtree.exe"
model = "GTR+F+I+G4"
bootstrap = "-bb 1000"

files = glob.glob(os.path.join(folder, "O_singlerandom_*.fasta"))

def run_iqtree(fasta_file):
    command = f'"{exe}" -s "{fasta_file}" -m {model} {bootstrap}'
    print(f"Запускаю: {command}")
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    num_cores = os.cpu_count()
    num_processes = max(1, num_cores - 1) 

    with Pool(processes=num_processes) as pool:
        pool.map(run_iqtree, files)

    print("Все задачи завершены.")
