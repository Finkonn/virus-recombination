import subprocess
import os

serotypes = ["A", "Asia1", "C", "O", "SAT1", "SAT2", "SAT3"]
regions = ["Lpro", "P1", "P2", "P3"]
output_file = "median_heights.csv"

with open(output_file, 'w') as file:
    file.write("Serotype,Region1,Region2,Median Height\n")

for serotype in serotypes:
    tree1_path = os.path.join("MCC", f"{serotype}_P1.tree")
    
    for region in regions:
        tree2_path = os.path.join(region, f"{serotype}.treefile")
        
        cmd = [
            "python", "halflife.py",
            "-tree1", tree1_path,
            "-tree2", tree2_path,
            "-pthr", "0.8",
            "-serotype", serotype,
            "-region", region,
            "-output", output_file
        ]
        subprocess.run(cmd)
