import argparse
import pandas as pd

def color_nexus(excel_file, nexus_input_file, nexus_output_file, color="#FF0000"):
    df = pd.read_excel(excel_file)

    accessions = set()
    for num, value in enumerate(df['Match']):
        if value == 'Yes':
            accessions.add(df['Accession no.'].iloc[num])

    with open(nexus_input_file, 'r') as file:
        nexus_lines = file.readlines()

    with open(nexus_output_file, 'w') as output_file:
        for line in nexus_lines:
            if line.strip().startswith(tuple(accessions)):
                start = line.find("[&!color=")
                if start != -1:
                    end = line.find("]", start)
                    if end != -1:
                        line = line[:start + 9] + color + line[end:]
            output_file.write(line)

    print(f"Updated Nexus file saved to: {nexus_output_file}")

def main():
    parser = argparse.ArgumentParser(description='Color lines in a Nexus file based on accessions matched in an Excel file.')
    parser.add_argument('-e', '--excel', required=True, help='Input Excel file with accession numbers.')
    parser.add_argument('-n', '--nexus_input', required=True, help='Input Nexus file to be colored.')
    parser.add_argument('-o', '--nexus_output', required=True, help='Output Nexus file with the updated colors.')
    parser.add_argument('-c', '--color', default="#FF0000", help='Color code to apply to matching accessions (default: #FF0000 for red).')

    args = parser.parse_args()

    color_nexus(args.excel, args.nexus_input, args.nexus_output, args.color)

if __name__ == '__main__':
    main()
