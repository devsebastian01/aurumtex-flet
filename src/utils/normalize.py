
import unicodedata

import pandas as pd


def normalize_text(text: str) -> str:
    text = str(text).lower().strip()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text

def normalize_keys(data: list[dict]) -> list[dict]:
    normalized_data = []

    for row in data:
        new_row = {}
        for key, value in row.items():
            normalized_key = normalize_text(key)
            new_row[normalized_key] = value
        normalized_data.append(new_row)

    return normalized_data

def normalize_headers(header_list: list[str]) -> list[str]:
    normalized_headers = []
    for header in header_list:
        normalized_header = normalize_text(header)
        normalized_headers.append(normalized_header)
    return normalized_headers

def normalize_dataframe_columns(df: pd.DataFrame) -> list:
    normalized_columns = []
    for col in df.columns:
        normalized_columns.append(normalize_text(col))
    return normalized_columns