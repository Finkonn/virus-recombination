import os
import subprocess
import glob
from multiprocessing import Pool

base_folder = "Recomb_free_sequences"
exe = "bin/iqtree3.exe"
model = "GTR+F+I+G4"
bootstrap = "-bb 1000"

pattern = os.path.join(base_folder, "recomb_free_*", "*.fasta")
files = glob.glob(pattern)

def run_iqtree(fasta_file):
    command = f'"{exe}" -s "{fasta_file}" -m {model} {bootstrap}'
    print(f"Launching: {command}")
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    num_cores = os.cpu_count()
    num_processes = max(1, num_cores - 1)

    with Pool(processes=num_processes) as pool:
        pool.map(run_iqtree, files)

    print("All tasks completed.")
