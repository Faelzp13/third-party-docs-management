import pandas as pd
import numpy as np
from datetime import datetime
from parsers.utils import enforce_schema


def parse_newera(bronze_filepath: str) -> pd.DataFrame:
    df = pd.read_excel(bronze_filepath)
    df.columns = [str(col).strip().lower().replace(' ', '_') for col in df.columns]

    column_mapping = {
        'documentos': 'document_name',
        'vencimento': 'due_date',
        'responsável': 'responsible_company',
        'unnamed:_16': 'branch',
        'situação': 'status',
        'unnamed:_18': 'coluna_s_suja'
    }
    df_clean = df.rename(columns=column_mapping)

    if 'document_name' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['document_name'])

    if 'coluna_s_suja' in df_clean.columns:
        is_competence = df_clean['coluna_s_suja'].astype(str).str.contains(r'COMP_|\d{2}/\d{4}', regex=True, case=False,
                                                                           na=False)

        df_clean['competence_date'] = np.where(is_competence, df_clean['coluna_s_suja'], None)
        df_clean['employee_name'] = np.where(~is_competence, df_clean['coluna_s_suja'], None)

    df_final = enforce_schema(df_clean)

    df_final['source_system'] = 'newera'
    df_final['ingestion_date'] = datetime.now()

    print(f"Success: {len(df_final)} Newera records cleaned.")
    return df_final


if __name__ == '__main__':
    import os

    raw_file = r'C:\Users\...'
    silver_dir = r'C:\Users\...'
    os.makedirs(silver_dir, exist_ok=True)
    silver_file = os.path.join(silver_dir, 'newera_cleaned.parquet')

    print("Starting Newera local test...")
    df_result = parse_newera(raw_file)
    print("\nFirst 10 cleaned rows:")
    print(df_result.head(10).to_string())
    df_result.to_parquet(silver_file, index=False)