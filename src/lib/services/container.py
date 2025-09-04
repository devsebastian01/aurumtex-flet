from src.lib.db.repositories.roll_repository import save_rolls_to_db
from src.utils.zpl import generate_zpl_pair, generate_zpl_single
from itertools import zip_longest
# import impresora
import win32print

def register_container(list_dict_excels, connection_db):
    list_rolls = {}
    for container, data_rolls in list_dict_excels.items():
        # Guardar rollos en BD y extraer los rollos guardados
        list_rolls[container] = save_rolls_to_db(data_rolls=data_rolls,
                                                container= container,
                                                connection_db= connection_db)


    # 3. Crear etiquetas zpl de codigos de barra
    all_zpl = ""
    for container, roll_list in list_rolls.items():
        try:
            filtered_rolls = []
            for roll in roll_list:
                if roll["container"] == container:
                    filtered_rolls.append(roll)
        
            it = iter(filtered_rolls)
            for roll1, roll2 in zip_longest(it, it):
                if roll2:
                    all_zpl += generate_zpl_pair(roll1, roll2)
                else:
                    all_zpl += generate_zpl_single(roll1)

            print(f"Info: Codigos de barras del contenedor {container} [Completado]")
        except Exception as e:
            print(f"Info: Codigos de barras del contenedor {container} [Fallido]", e)


    # 4. Enviar etiqueta zpl a impresora
    printer_name = "impresora despachos"
    zpl_data = all_zpl
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        job_info = ("Etiqueta ZPL", None, "RAW")  # RAW es obligatorio para ZPL
        job = win32print.StartDocPrinter(hPrinter, 1, job_info)
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, zpl_data.encode("utf-8"))
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        print("Info: Etiquetas enviadas a impresora [Completado]")
    except Exception as e:
        raise Exception("Info: Etiquetas enviadas a impresora [Fallido]")
    finally:
        win32print.ClosePrinter(hPrinter)
