import pandas as pd
from datetime import datetime

def parse_afm(bronze_filepath: str) -> pd.DataFrame:

    # read the excel file
    df = pd.read_excel(bronze_filepath, skiprows=15)

    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]

    if 'unnamed:_0' in df.columns:
        df = df.drop(columns=['unnamed:_0'])

    if 'documento' in df.columns:
        df = df.dropna(subset=['documento'])

    column_mapping = {
        'documento': 'document_name',
    }
    df_clean = df.rename(columns=column_mapping)

    standard_columns = [
        'employee_name',
        'due_date',
        'competence_date',
        'document_code',
        'document_name',
        'status',
        'responsible_company',
        'branch'
    ]

    for col in standard_columns:
        if col not in df_clean.columns:
            df_clean[col] = None

    df_final = df_clean[standard_columns].copy()

    df_final['source_system'] = 'afm'
    df_final['ingestion_date'] = datetime.now()

    print(f"Success: {len(df_final)} AFM records cleaned.")
    return df_final


if __name__ == '__main__':
    import os

    # raw file path
    raw_file = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\01_bronze\afm\Relatorio - Entrega de documentos - 260602114741.xlsx'

    # silver directory path
    silver_dir = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\02_silver\afm'
    os.makedirs(silver_dir, exist_ok=True)

    silver_file = os.path.join(silver_dir, 'afm_cleaned.parquet')

    print("Starting AFM local test...")
    df_result = parse_afm(raw_file)

    print("\nFirst 5 cleaned rows:")
    print(df_result.head().to_string())

    # save the file
    df_result.to_parquet(silver_file, index=False)
    print(f"\nFile successfully saved to: {silver_file}")