import os

def replace_underscores_in_treefiles(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".treefile"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                content = file.read()
            
            modified_content = content.replace("_", "/")
            
            with open(filepath, 'w') as file:
                file.write(modified_content)
            
            print(f"Processed: {filename}")

# Specify the directory containing .treefile files
directory = "./"  # Change this if needed
replace_underscores_in_treefiles(directory)
