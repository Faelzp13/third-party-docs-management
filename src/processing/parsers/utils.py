import pandas as pd


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
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
        if col not in df.columns:
            df[col] = None

    return df[standard_columns].copy()