import pandas as pd
import os

def remove_rows_by_genbank_accession(input_file, output_file):
    
    df_first_sheet = pd.read_excel(input_file, sheet_name=0)
    df_third_sheet = pd.read_excel(input_file, sheet_name=2)
    
    remove_mask = df_third_sheet['keep_remove'].astype(str).str.lower().str.strip() == 'remove'
    rows_to_remove = df_third_sheet[remove_mask].copy()
    
    accession_to_remove = rows_to_remove['Genbank accession'].tolist()
    
    mask_to_remove = df_first_sheet['Genbank accession'].isin(accession_to_remove)
    rows_being_removed = df_first_sheet[mask_to_remove]
    
    df_filtered = df_first_sheet[~mask_to_remove].copy()
    df_filtered = df_filtered.drop(columns=['Genbank accession'], errors='ignore')
    df_filtered.to_excel(output_file, index=False)
    
    report_file = output_file.replace('.xlsx', '_removed_seqs.xlsx')
    rows_being_removed.to_excel(report_file, index=False)
    
    print(f"Удалено строк: {len(rows_being_removed)}")
    print(f"Осталось строк: {len(df_filtered)}")
    
    return True

if __name__ == "__main__":
    input_file = "metadata_references_iso_source.xlsx" 
    output_file = "meta_no_probang.xlsx"  
    
    remove_rows_by_genbank_accession(input_file, output_file)