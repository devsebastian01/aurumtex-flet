import os
from src.utils.handle_bd import get_list_import_rolls
from src.lib.db.db_connection import connection_db
from src.utils.create_pdf import create_group_invoice_pdf, create_non_group_invoice_pdf
from src.utils.group_rolls import group_by_color


list_roll = [
    {"color": "CAMEL OSCURO", "roll": "9"},
    {"color": "CAMEL OSCURO", "roll": "7"},
    {"color": "CAMEL OSCURO", "roll": "2"},
    {"color": "CAMEL OSCURO", "roll": "20"},
    {"color": "CAMEL OSCURO", "roll": "21"},
    {"color": "CAMEL OSCURO", "roll": "1"},

    {"color": "CAFE", "roll": "11"},
    {"color": "CAFE", "roll": "3"},
    {"color": "CAFE", "roll": "14"},

    {"color": "CAMEL CALORO", "roll": "18"},
    {"color": "CAMEL CALORO", "roll": "21"},
    {"color": "CAMEL CALORO", "roll": "1"},
    {"color": "CAMEL CALORO", "roll": "5"},

    {"color": "AZUL OSCURO", "roll": "5"},
    {"color": "AZUL OSCURO", "roll": "119"},
    {"color": "AZUL OSCURO", "roll": "12"},
    {"color": "AZUL OSCURO", "roll": "50"},
    {"color": "AZUL OSCURO", "roll": "40"},
    {"color": "AZUL OSCURO", "roll": "15"},
    {"color": "AZUL OSCURO", "roll": "57"},
    {"color": "AZUL OSCURO", "roll": "58"},
    {"color": "AZUL OSCURO", "roll": "38"},
    {"color": "AZUL OSCURO", "roll": "48"},
    {"color": "AZUL OSCURO", "roll": "21"},
    {"color": "AZUL OSCURO", "roll": "11"},
    {"color": "AZUL OSCURO", "roll": "19"},
    {"color": "AZUL OSCURO", "roll": "105"},
    {"color": "AZUL OSCURO", "roll": "34"},
    {"color": "AZUL OSCURO", "roll": "113"},
    {"color": "AZUL OSCURO", "roll": "43"},
    {"color": "AZUL OSCURO", "roll": "116"},
    {"color": "AZUL OSCURO", "roll": "112"},
    {"color": "AZUL OSCURO", "roll": "53"},

    {"color": "ROJO", "roll": "43"},
    {"color": "ROJO", "roll": "21"},
    {"color": "ROJO", "roll": "35"},
    {"color": "ROJO", "roll": "15"},
    {"color": "ROJO", "roll": "20"},
    {"color": "ROJO", "roll": "7"},
    {"color": "ROJO", "roll": "22"},
    {"color": "ROJO", "roll": "5"},
    {"color": "ROJO", "roll": "42"},
    {"color": "ROJO", "roll": "48"},
    {"color": "ROJO", "roll": "49"},
    {"color": "ROJO", "roll": "8"},
    {"color": "ROJO", "roll": "30"},
    {"color": "ROJO", "roll": "19"},


    {"color": "AZUL REY", "roll": "17"},
    {"color": "AZUL REY", "roll": "9"},
    {"color": "AZUL REY", "roll": "5"},
    {"color": "AZUL REY", "roll": "8"},

    {"color": "VERDE CALI", "roll": "17"},
    {"color": "VERDE CALI", "roll": "26"},
    {"color": "VERDE CALI", "roll": "57"},
    {"color": "VERDE CALI", "roll": "52"},
    {"color": "VERDE CALI", "roll": "55"},
    {"color": "VERDE CALI", "roll": "28"},
    {"color": "VERDE CALI", "roll": "12"},
    {"color": "VERDE CALI", "roll": "7"},
    {"color": "VERDE CALI", "roll": "4"},
    {"color": "VERDE CALI", "roll": "40"},
    {"color": "VERDE CALI", "roll": "39"},
    {"color": "VERDE CALI", "roll": "29"},
    {"color": "VERDE CALI", "roll": "54"},
    {"color": "VERDE CALI", "roll": "50"},

    {"color": "NEGRO", "roll": "47"},
    {"color": "NEGRO", "roll": "100"},
    {"color": "NEGRO", "roll": "138"},
    {"color": "NEGRO", "roll": "20"},
    {"color": "NEGRO", "roll": "70"},
    {"color": "NEGRO", "roll": "7"},
    {"color": "NEGRO", "roll": "35"},
    {"color": "NEGRO", "roll": "36"},
    {"color": "NEGRO", "roll": "52"},
    {"color": "NEGRO", "roll": "145"},
    {"color": "NEGRO", "roll": "132"},
    {"color": "NEGRO", "roll": "123"},
    {"color": "NEGRO", "roll": "125"},
    {"color": "NEGRO", "roll": "80"},
    {"color": "NEGRO", "roll": "65"},
    {"color": "NEGRO", "roll": "130"},
    {"color": "NEGRO", "roll": "131"},
    {"color": "NEGRO", "roll": "147"},
    {"color": "NEGRO", "roll": "18"},
    {"color": "NEGRO", "roll": "156"},
    {"color": "NEGRO", "roll": "21"},
    {"color": "NEGRO", "roll": "149"},
    {"color": "NEGRO", "roll": "28"},
    {"color": "NEGRO", "roll": "148"},

    {"color": "NEGRO", "roll": "13"},
    {"color": "NEGRO", "roll": "118"},
    {"color": "NEGRO", "roll": "93"},
    {"color": "NEGRO", "roll": "82"},
    {"color": "NEGRO", "roll": "61"},
    {"color": "NEGRO", "roll": "95"},

    {"color": "BLANCO OPTICO", "roll": "7"},
    {"color": "BLANCO OPTICO", "roll": "8"},
    {"color": "BLANCO OPTICO", "roll": "28"},
    {"color": "BLANCO OPTICO", "roll": "16"},
    {"color": "BLANCO OPTICO", "roll": "91"},
    {"color": "BLANCO OPTICO", "roll": "71"},
    {"color": "BLANCO OPTICO", "roll": "1"},
    {"color": "BLANCO OPTICO", "roll": "84"},
    {"color": "BLANCO OPTICO", "roll": "88"},
    {"color": "BLANCO OPTICO", "roll": "85"},
    {"color": "BLANCO OPTICO", "roll": "95"},
    {"color": "BLANCO OPTICO", "roll": "94"},
    {"color": "BLANCO OPTICO", "roll": "41"},
    {"color": "BLANCO OPTICO", "roll": "34"},
    {"color": "BLANCO OPTICO", "roll": "19"},
    {"color": "BLANCO OPTICO", "roll": "73"},
    {"color": "BLANCO OPTICO", "roll": "15"},
    {"color": "BLANCO OPTICO", "roll": "76"},
    {"color": "BLANCO OPTICO", "roll": "92"},
    {"color": "BLANCO OPTICO", "roll": "2"},
    {"color": "BLANCO OPTICO", "roll": "82"},
    {"color": "BLANCO OPTICO", "roll": "83"},
    {"color": "BLANCO OPTICO", "roll": "78"},
    {"color": "BLANCO OPTICO", "roll": "87"},
    {"color": "BLANCO OPTICO", "roll": "50"},
    {"color": "BLANCO OPTICO", "roll": "93"},
    {"color": "BLANCO OPTICO", "roll": "57"},
    {"color": "BLANCO OPTICO", "roll": "49"},
    {"color": "BLANCO OPTICO", "roll": "44"},
    {"color": "BLANCO OPTICO", "roll": "36"}
]



conn = connection_db()

all_list_rolls =get_list_import_rolls(connection_db=conn)



check_rolls = []
for roll in all_list_rolls:
    if roll["checked"]:
        check_rolls.append(roll)


# 5) Generar PDFs
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
create_non_group_invoice_pdf(
    client="",
    nit="",
    list_rolls=check_rolls,
    path_folder=downloads_path,
)
group_color = group_by_color(list_rolls=check_rolls)
create_group_invoice_pdf(
    client="",
    client_nit="",
    color_group=group_color,
    path_folder=downloads_path,
    note_number="AU-321",
)
