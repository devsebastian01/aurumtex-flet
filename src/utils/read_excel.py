from src.utils.normalize import normalize_dataframe_columns, normalize_keys, normalize_text
from collections import Counter
import pandas as pd
import os


def read_excel_by_headers(headers_model: list, document_files: list[str]):
    
    list_dict_excels = {}

    for document_path in document_files:
        dict_str_list = {}
        document_name = os.path.basename(document_path)  

        # Detectar extensión
        if document_path.endswith(".xlsx"):
            xls = pd.ExcelFile(document_path, engine="openpyxl")
        else:
            xls = pd.ExcelFile(document_path)

        for sheet_name in xls.sheet_names:
            df_raw = pd.read_excel(xls, sheet_name=sheet_name, header=None, dtype=str)
            header_row_idx = None

            for i, row in df_raw.iterrows():
                row_values = [normalize_text(str(cell)) for cell in row.values]

                if Counter(row_values) >= Counter(headers_model):
                    header_row_idx = i
                    type_model = headers_model
                    break

            if header_row_idx is None:
                print(
                    f"Info: Lectura de hoja: ['{sheet_name}'] del excel ['{document_name}'] [Fallido]"
                )
                continue

            # Releer con headers correctos
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_idx, dtype=str)
            df = df.fillna("")

            normalized_actual_columns = normalize_dataframe_columns(df)

            # Validar headers
            for header in type_model:
                if header not in normalized_actual_columns:
                    raise ValueError(
                        f"In file '{document_name}', sheet '{sheet_name}', "
                        f"can't find header: '{header}'"
                    )

            sheet_key = normalize_text(sheet_name)
            data_as_dict = df.to_dict(orient="records")
            normalized_data = normalize_keys(data_as_dict)

            dict_str_list[sheet_key] = normalized_data

        list_dict_excels = dict_str_list

    return list_dict_excels


def read_general_excel_to_list(path_file: str) -> list[dict]:
    list_dict_index = []

    if path_file.endswith('.xlsx'):
        xls = pd.ExcelFile(path_file, engine='openpyxl')
    else:
        xls = pd.ExcelFile(path_file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
        df = df.fillna("")
        # df = xls.parse(sheet_name)
        list_dict_index.append(df.to_dict('index'))
    if len(list_dict_index) <= 0:
        return []
    list_dict = []
    for i in list_dict_index[0].keys():
        list_dict.append(list_dict_index[0][i])

    return list_dict