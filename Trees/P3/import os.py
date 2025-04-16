import os

filepath = "recomb_free_P1.treefile"
with open(filepath, 'r') as file:
    content = file.read()

    modified_content = content.replace("_", "/")

    with open(filepath, 'w') as file:
        file.write(modified_content)

