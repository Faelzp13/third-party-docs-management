import os
import glob
import pandas as pd

# Importing our 4 engines (parsers)
from parsers.gt3soft_parser import parse_gt3soft
from parsers.afm_parser import parse_afm
from parsers.newera_parser import parse_newera
from parsers.sg3_parser import parse_sg3


def find_latest_file(folder_path: str, extension: str = '*.*') -> str:
    files = glob.glob(os.path.join(folder_path, extension))
    if not files:
        return None
    # Returns the most recently modified file
    return max(files, key=os.path.getmtime)


def run_pipeline(base_path: str):
    print("Starting Data Pipeline: Bronze -> Silver -> Gold\n")

    bronze_path = os.path.join(base_path, 'data', '01_bronze')
    silver_path = os.path.join(base_path, 'data', '02_silver')
    gold_path = os.path.join(base_path, 'data', '03_gold')

    os.makedirs(gold_path, exist_ok=True)

    all_clean_dfs = []

    print("--- Processing GT3Soft ---")
    gt3_file = find_latest_file(os.path.join(bronze_path, 'gt3soft'), '*.xls')
    if gt3_file:
        df_gt3 = parse_gt3soft(gt3_file)
        df_gt3.to_parquet(os.path.join(silver_path, 'gt3soft', 'gt3soft_cleaned.parquet'), index=False)
        all_clean_dfs.append(df_gt3)

    print("\n--- Processing AFM ---")
    afm_file = find_latest_file(os.path.join(bronze_path, 'afm'), '*.xlsx')
    if afm_file:
        df_afm = parse_afm(afm_file)
        df_afm.to_parquet(os.path.join(silver_path, 'afm', 'afm_cleaned.parquet'), index=False)
        all_clean_dfs.append(df_afm)

    print("\n--- Processing Newera ---")
    newera_file = find_latest_file(os.path.join(bronze_path, 'newera'), '*.xlsx')
    if newera_file:
        df_newera = parse_newera(newera_file)
        df_newera.to_parquet(os.path.join(silver_path, 'newera', 'newera_cleaned.parquet'), index=False)
        all_clean_dfs.append(df_newera)

    print("\n--- Processing SG3 ---")
    sg3_file = find_latest_file(os.path.join(bronze_path, 'sg3'), '*.xlsx')
    if sg3_file:
        df_sg3 = parse_sg3(sg3_file)
        df_sg3.to_parquet(os.path.join(silver_path, 'sg3', 'sg3_cleaned.parquet'), index=False)
        all_clean_dfs.append(df_sg3)

    # The Great Union
    print("\n--- Building Gold Layer (Single Big Table) ---")
    if all_clean_dfs:
        # Stacking all DataFrames into one
        df_gold = pd.concat(all_clean_dfs, ignore_index=True)

        # Saving the master consolidated file
        gold_file = os.path.join(gold_path, 'consolidated_documents.parquet')
        df_gold.to_parquet(gold_file, index=False)

        print(f"Success! Single Big Table created with {len(df_gold)} documents.")
        print(f"File saved to: {gold_file}")
    else:
        print("No data was processed. Check your Bronze layer files.")


if __name__ == '__main__':
    PROJETO_RAIZ = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management'

    run_pipeline(PROJETO_RAIZ)