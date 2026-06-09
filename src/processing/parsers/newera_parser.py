import pandas as pd
from datetime import datetime

def parse_newera(bronze_filepath: str) -> pd.DataFrame:

    # read the excel file
    df = pd.read_excel(bronze_filepath)

    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]

    column_mapping = {
        'documentos': 'document_name',
        'vencimento': 'due_date',
        'unnamed:_18': 'employee_name'
    }
    df_clean = df.rename(columns=column_mapping)

    if 'document_name' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['document_name'])

    standard_columns = ['employee_name', 'due_date', 'document_code', 'document_name']
    for col in standard_columns:
        if col not in df_clean.columns:
            df_clean[col] = None

    df_final = df_clean[standard_columns].copy()

    df_final['source_system'] = 'newera'
    df_final['ingestion_date'] = datetime.now()

    print(f"Success: {len(df_final)} Newera records cleaned.")
    return df_final


if __name__ == '__main__':
    import os

    # raw file path
    raw_file = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\01_bronze\newera\Elaboração RECICLA ENGENHARIA E GESTAO AMBIENTAL LTDA .xlsx'

    # silver directory path
    silver_dir = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\02_silver\newera'
    os.makedirs(silver_dir, exist_ok=True)

    silver_file = os.path.join(silver_dir, 'newera_cleaned.parquet')

    print("Starting Newera local test...")
    df_result = parse_newera(raw_file)

    print("\nFirst 5 cleaned rows:")
    print(df_result.head().to_string())

    # save the file
    df_result.to_parquet(silver_file, index=False)
    print(f"\nFile successfully saved to: {silver_file}")