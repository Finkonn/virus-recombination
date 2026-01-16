import re

def process_nexus_file(input_file, output_file):
    reference_colors = {}  
    sequences = [] 

    color_pattern = re.compile(r"\[&!color=(?P<color>#\w+)\]")

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  
            if not line or ";" in line:  
                continue

            parts = line.split("_")
            if len(parts) < 2:
                continue

            name = parts[0]
            second_part = parts[1]
            last_part = parts[-1]

            if second_part in {"O", "A", "Asia1", "SAT1", "SAT2", "SAT3", "C"}:
                topotype = last_part.split("[")[0]  
                match = color_pattern.search(line)
                if match:
                    color = match.group("color")
                    reference_colors[color] = topotype
            else:
                match = color_pattern.search(line)
                if match:
                    color = match.group("color")
                    sequences.append((line, color)) 

    with open(output_file, 'w') as file:
        for seq, color in sequences:
            if color in reference_colors:
                topotype = reference_colors[color]
                cleaned_seq = re.sub(r"\[&!color=#\w+\]", "", seq)
                file.write(f"{cleaned_seq}_{topotype}\n")

input_nexus_file = "../Trees/Colored/VP1_topotype_colored.nexus"  
output_file = "genotyped_topotypes.txt" 
process_nexus_file(input_nexus_file, output_file)
