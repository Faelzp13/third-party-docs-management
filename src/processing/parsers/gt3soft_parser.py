import pandas as pd
from datetime import datetime

def parse_gt3soft(bronze_filepath: str) -> pd.DataFrame:

    # read excel file
    df = pd.read_excel(bronze_filepath, header=None)

    is_person_row = df[1].astype(str).str.contains('Pessoa:', na=False, case=False)

    df.loc[is_person_row, 'employee_name'] = df[4]

    df['employee_name'] = df['employee_name'].ffill()

    df['employee_name'] = df['employee_name'].astype(str).str.replace(r'\.0$', '', regex=True)

    df_clean = df.dropna(subset=[7]).copy()

    df_clean = df_clean[~df_clean[2].astype(str).str.contains('Data Venc', na=False, case=False)]

    df_clean = df_clean.rename(columns={
        2: 'due_date',
        5: 'document_code',
        7: 'document_name'
    })

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

    df_final['source_system'] = 'gt3soft'
    df_final['ingestion_date'] = datetime.now()

    print(f"Success: {len(df_final)} GT3Soft records flattened and cleaned.")
    return df_final


if __name__ == '__main__':
    import os

    # raw file path
    raw_file = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\01_bronze\gt3soft\20260602_164856_11674.xls'

    # silver directory path
    silver_dir = r'C:\Users\TI Recicla\PycharmProjects\third-party-docs-management\data\02_silver\gt3soft'
    os.makedirs(silver_dir, exist_ok=True)

    silver_file = os.path.join(silver_dir, 'gt3soft_cleaned.parquet')

    print("Starting GT3Soft local test...")
    df_result = parse_gt3soft(raw_file)

    print("\nFirst 5 cleaned rows:")
    print(df_result.head().to_string())

    # save the file
    df_result.to_parquet(silver_file, index=False)
    print(f"\nFile successfully saved to: {silver_file}")