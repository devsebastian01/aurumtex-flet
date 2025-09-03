import uuid
from psycopg2.extras import execute_values

def search_info_roll(uuid_roll_search: str, connection_db):
    try:
        cursor = connection_db.cursor()

        query = """
            SELECT uuid, item, roll, color, siigo_code, mts, kg, container, checked
            FROM roll
            WHERE uuid = %s
        """
        cursor.execute(query, (uuid_roll_search,))
        result = cursor.fetchone()

        cursor.close()

        if result:

            return {
                "uuid": result[0],
                "item": result[1],
                "roll": result[2],
                "color": result[3],
                "siigo_code": result[4],
                "mts": float(result[5]),
                "kg": float(result[6]),
                "container": result[7],
                "checked": result[8]
            }
        else:
            return None

    except Exception as e:
        print(f"Error al buscar el roll con uuid {uuid_roll_search}: {e}")
        return None
    

def verify_check_roll(uuid_roll_search: str, connection_db) -> bool:
    try:
        cursor = connection_db.cursor()

        query = """
            SELECT checked
            FROM roll
            WHERE uuid = %s
        """
        cursor.execute(query, (uuid_roll_search,))
        result = cursor.fetchone()

        cursor.close()

        if result is None:
            # No existe el roll en la BD
            return False

        checked = result[0]
        if checked:
            return False
        
        return True

    except Exception as e:
        print(f"Error al verificar el roll con uuid {uuid_roll_search}: {e}")
        return False


def register_check_roll(uuid_roll_search: str, connection_db) -> bool:
    try:
        cursor = connection_db.cursor()

        query = """
            UPDATE roll
            SET checked = TRUE
            WHERE uuid = %s
            RETURNING uuid;
        """
        cursor.execute(query, (uuid_roll_search,))
        result = cursor.fetchone()

        connection_db.commit()
        cursor.close()

        if result is None:
            # No encontró el roll con ese UUID
            return False

        return True  # Se actualizó correctamente

    except Exception as e:
        connection_db.rollback()
        print(f"Error al registrar el check del roll {uuid_roll_search}: {e}")
        return False


def get_uuid_client_by_nit(nit_client_search, connection_db):
    try:
        cursor = connection_db.cursor()

        query = """
            SELECT uuid
            FROM client
            WHERE nit_client = %s
        """
        cursor.execute(query, (nit_client_search,))
        result = cursor.fetchone()

        cursor.close()

        if result:

            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Error al buscar el cliente con nit {nit_client_search}: {e}")
        return None


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


def save_invoice_to_db(invoice_rolls: list[dict], id_invoice: str, nit_client: str, connection_db) -> None:
    try:
        cursor = connection_db.cursor()
        values = []
        uuid_client = get_uuid_client_by_nit(nit_client_search = nit_client, 
                                             connection_db= connection_db)
        uuid_invoice = str(uuid.uuid4()).replace('-', '')[:7]
        checked= False
        for roll in invoice_rolls:    
            uuid_roll = roll.get("uuid", None)
            # Valores para la bd
            values.append((uuid_invoice, id_invoice, uuid_roll, uuid_client,checked))
        
        # Cargar todos la lista de los valores en la bd de manera masiva
        execute_values(cursor, """
            INSERT INTO invoice (uuid, id_invoice, uuid_roll, uuid_client, checked)
            VALUES %s
        """, values)

        connection_db.commit()
        cursor.close()
        print(f"Info: Facturando {len(invoice_rolls)} rollos para el cliente {nit_client} en BD [Completado]")
        
    except Exception as e:
        connection_db.rollback()
        print(f"Info: Facturando {len(invoice_rolls)} rollos para el cliente {nit_client} en BD [Fallido]")


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