import uuid
from psycopg2.extras import execute_values



# Extrae todos los rollos de la bd y los convierte en un dict
def get_list_import_rolls(connection_db):
    try:
        
        cursor = connection_db.cursor()
        cursor.execute("SELECT * FROM roll")
        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(col_names, row)) for row in rows]
        return result
    except Exception as e:
        connection_db.rollback()
        print(f"Info: Listado de rollos [Fallido]: {e}")
        return []


# Guarda una lista de rollos en la bd
def save_rolls_to_db(data_rolls: list[dict], container: str, connection_db) -> None:
    try:
        cursor = connection_db.cursor()
        values = []
        list_rolls = []

        for data in data_rolls:
            item = data.get("item", None)
            roll = data.get("roll no", None)
            color = data.get("color", None)
            siigo_code = data.get("codigo siigo", None)

            mts = round(float(data.get("mts", 0)), 2)
            kg = round(float(data.get("kg", 0)), 2)
            roll = int(float(roll))
            uid = str(uuid.uuid4()).replace("-", "")[:7]
            check = False

            # Valores para la BD
            values.append((uid, item, roll, color, siigo_code, mts, kg, container, check))

            # Datos estructurados
            info_roll = {
                "item": item,
                "roll": roll,
                "color": color,
                "mts": mts,
                "kg": kg,
                "siigo_code": siigo_code,
                "container": container,
                "uuid": uid,
                "check": check,
            }
            list_rolls.append(info_roll)

        # Insertar en BD
        execute_values(
            cursor,
            """
            INSERT INTO roll (uuid, item, roll, color, siigo_code, mts, kg, container, checked)
            VALUES %s
        """,
            values,
        )
        connection_db.commit()
        cursor.close()
        print(f"Info: Guardando {len(data_rolls)} rollos del contenedor {container} en BD [Completado]")

        return list_rolls

    except Exception as e:
        connection_db.rollback()
        print(f"Info: Guardando {len(data_rolls)} rollos del contenedor {container} en BD [Fallido]: {e}")


# Actualiza los valores de una lista con los uuid de los rollos que se quieren marcar con true
def update_rolls_checked(cursor, barcode_list, checked=True):
    placeholders = ",".join(["%s"] * len(barcode_list))
    sql = f"UPDATE roll SET checked = %s WHERE uuid IN ({placeholders})"
    cursor.execute(sql, tuple([checked] + barcode_list))


# 
def select_rolls_by_uuid(cursor, barcode_list):
    placeholders = ",".join(["%s"] * len(barcode_list))
    sql = (
        f"SELECT uuid, roll, item, color, mts, kg, siigo_code, container "
        f"FROM roll WHERE uuid IN ({placeholders})"
    )
    cursor.execute(sql, tuple(barcode_list))
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]
