import os
from pathlib import Path
import pandas as pd
from Bio import SeqIO
import argparse

# Словарь для сокращения топотипов
TOPOTYPE_ABBREV = {
    "EUROPE-SOUTH-AMERICA-EURO-SA-SOUTH": "EURO-SA",
    "EAST-AFRICA-1-EA-1": "EA-1",
    "EAST-AFRICA-2-EA-2": "EA-2", 
    "EAST-AFRICA-3-EA-3": "EA-3",
    "EAST-AFRICA-4-EA-4": "EA-4",
    "I-NORTHWEST-ZIMBABWE-NWZ": "I-NWZ",
    "I-SOUTHEAST-ZIMBABWE-SEZ": "I-SEZ",
    "III-NORTHWEST-ZIMBABWE-NWZ": "III-NWZ",
    "II-WESTERN-ZIMBABWE-WZ": "II-WZ",
    "III-WESTERN-ZIMBABWE-WZ": "III-WZ",
    "INDONESIA-1-ISA-1-1": "ISA-1",
    "IV-EAST-AFRICA1-EA-1": "IV-EA-1",
    "MIDDLE-EAST-SOUTH-ASIA-ME-SA": "ME-SA",
    "V-East-Africa-EA": "V-EA",
    "VII-EAST-AFRICA-2-EA-2": "VII-EA-2",
    "WEST-AFRICA-WA": "WA",
    "SOUTHEAST-ASIA-SEA": "SEA",
    "EUROPE-SOUTH-AMERICA-EURO-SA": "EURO-SA"
}

def load_metadata(metadata_file):
    df = pd.read_excel(metadata_file)
    metadata_dict = {}
    
    for _, row in df.iterrows():
        accession = str(row['Genbank accession']).strip()
        if pd.isna(accession) or accession == '':
            continue
        
        # Получаем значения с заменой NaN на Unknown
        country = str(row['Country']).strip() if pd.notna(row['Country']) else 'Unknown'
        host = str(row['Host']).strip() if pd.notna(row['Host']) else 'Unknown'
        year = str(row['Year']).strip() if pd.notna(row['Year']) else 'Unknown'
        serotype = str(row['Serotype']).strip() if pd.notna(row['Serotype']) else 'Unknown'
        
        # Топотип и линия с сокращением
        topotype_raw = str(row['Topotype']).strip() if pd.notna(row['Topotype']) else 'Unknown'
        topotype = TOPOTYPE_ABBREV.get(topotype_raw, topotype_raw)
        
        lineage = str(row['Lineage']).strip() if pd.notna(row['Lineage']) else 'Unknown'
        
        metadata_dict[accession] = {
            'country': country,
            'host': host,
            'year': year,
            'serotype': serotype,
            'topotype': topotype,
            'lineage': lineage
        }
    
    return metadata_dict

def process_fasta_file(fasta_path, metadata_dict):
    records = list(SeqIO.parse(fasta_path, "fasta"))
    updated = 0
    
    for record in records:
        parts = record.id.split('/')
        if parts:
            accession = parts[0]
            if accession in metadata_dict:
                meta = metadata_dict[accession]
                # Новый формат: GenbankAccession/country/host/year/serotype/topotype/lineage
                new_id = f"{accession}/{meta['country']}/{meta['host']}/{meta['year']}/{meta['serotype']}/{meta['topotype']}/{meta['lineage']}"
                # Сохраняем дополнительные части после 5-го элемента
                if len(parts) > 5:
                    new_id += '/' + '/'.join(parts[5:])
                record.id = new_id
                record.description = ''
                updated += 1
    
    SeqIO.write(records, fasta_path, "fasta")
    return len(records), updated

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metadata', required=True, help='Metadata xlsx file')
    parser.add_argument('-d', '--directory', required=True, help='Directory with FASTA files')
    args = parser.parse_args()

    metadata_dict = load_metadata(args.metadata)
    
    fasta_files = list(Path(args.directory).rglob('*.fasta'))
    total_seqs = 0
    total_updated = 0
    
    for fasta_file in fasta_files:
        print(f"Processing: {fasta_file}")
        seqs, updated = process_fasta_file(fasta_file, metadata_dict)
        total_seqs += seqs
        total_updated += updated
        print(f"  Updated {updated}/{seqs} headers")
    
    print(f"\nTotal: {total_updated}/{total_seqs} headers updated")

if __name__ == "__main__":
    main()