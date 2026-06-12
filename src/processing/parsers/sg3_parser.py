import pandas as pd
from datetime import datetime
from parsers.utils import enforce_schema

def parse_sg3(bronze_filepath: str) -> pd.DataFrame:

    # 1. Read the excel file
    df = pd.read_excel(bronze_filepath)

    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]

    column_mapping = {
        'colaborador': 'employee_name',
        'documento': 'document_name',
        'competência': 'competence_date',
        'status': 'status',
        'empresa terceira': 'responsible_company',
        'estabelecimento': 'branch'
    }
    df_clean = df.rename(columns=column_mapping)

    if 'document_name' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['document_name'])

    df_final = enforce_schema(df_clean)

    df_final['source_system'] = 'sg3'
    df_final['ingestion_date'] = datetime.now()

    print(f"Success: {len(df_final)} SG3 records cleaned.")
    return df_final


if __name__ == '__main__':
    import os

    # raw file path
    raw_file = r'C:\Users\...'

    # silver directory path
    silver_dir = r'C:\Users\...'
    os.makedirs(silver_dir, exist_ok=True)

    silver_file = os.path.join(silver_dir, 'sg3_cleaned.parquet')

    print("Starting SG3 local test...")
    df_result = parse_sg3(raw_file)


    print("\nFirst 5 cleaned rows:")
    print(df_result.head().to_string())

    # save file
    df_result.to_parquet(silver_file, index=False)
    print(f"\nFile successfully saved to: {silver_file}")