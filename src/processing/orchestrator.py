import os
import glob
import pandas as pd

# importing all parsers
from parsers.gt3soft_parser import parse_gt3soft
from parsers.afm_parser import parse_afm
from parsers.newera_parser import parse_newera
from parsers.sg3_parser import parse_sg3


def find_latest_file(folder_path, extension="*.*"):
    # finds the newest file inside the folder
    files = glob.glob(os.path.join(folder_path, extension))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def run_pipeline(base_path):
    print("Starting pipeline execution")

    bronze_path = os.path.join(base_path, "data", "01_bronze")
    silver_path = os.path.join(base_path, "data", "02_silver")
    gold_path = os.path.join(base_path, "data", "03_gold")

    os.makedirs(gold_path, exist_ok=True)
    all_clean_dfs = []

    # processing gt3soft file
    print("Processing gt3soft")
    gt3_file = find_latest_file(os.path.join(bronze_path, "gt3soft"), "*.xls")
    if gt3_file:
        try:
            df_gt3 = parse_gt3soft(gt3_file)
            df_gt3.to_parquet(os.path.join(silver_path, "gt3soft", "gt3soft_cleaned.parquet"), index=False)
            all_clean_dfs.append(df_gt3)
        except Exception as e:
            print("Error processing gt3soft")
            print(e)

    # processing afm file
    print("Processing afm")
    afm_file = find_latest_file(os.path.join(bronze_path, "afm"), "*.xlsx")
    if afm_file:
        try:
            df_afm = parse_afm(afm_file)
            df_afm.to_parquet(os.path.join(silver_path, "afm", "afm_cleaned.parquet"), index=False)
            all_clean_dfs.append(df_afm)
        except Exception as e:
            print("Error processing afm")
            print(e)

    # processing newera file
    print("Processing newera")
    newera_file = find_latest_file(os.path.join(bronze_path, "newera"), "*.xlsx")
    if newera_file:
        try:
            df_newera = parse_newera(newera_file)
            df_newera.to_parquet(os.path.join(silver_path, "newera", "newera_cleaned.parquet"), index=False)
            all_clean_dfs.append(df_newera)
        except Exception as e:
            print("Error processing newera")
            print(e)

    # processing sg3 file
    print("Processing sg3")
    sg3_file = find_latest_file(os.path.join(bronze_path, "sg3"), "*.xlsx")
    if sg3_file:
        try:
            df_sg3 = parse_sg3(sg3_file)
            df_sg3.to_parquet(os.path.join(silver_path, "sg3", "sg3_cleaned.parquet"), index=False)
            all_clean_dfs.append(df_sg3)
        except Exception as e:
            print("Error processing sg3")
            print(e)

    # joining everything into gold folder
    print("Creating gold table")
    if all_clean_dfs:
        df_gold = pd.concat(all_clean_dfs, ignore_index=True)
        gold_file = os.path.join(gold_path, "consolidated_documents.parquet")
        df_gold.to_parquet(gold_file, index=False)
        print("Gold table created successfully")
    else:
        print("No files were processed")


if __name__ == "__main__":
    # automatic path finder using os
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    run_pipeline(project_root)