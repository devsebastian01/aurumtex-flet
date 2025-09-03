import os
import uuid
import random
from datetime import datetime
import psycopg2

from src.utils.handle_bd import get_uuid_client_by_nit
from src.utils.create_pdf import create_non_group_invoice_pdf, create_group_invoice_pdf
from src.utils.group_rolls import group_by_color

# Cola global para facturas que fallaron
failed_invoices = []


def _rows_to_dicts(cursor):
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


# Garantizar que la conexión esté abierta
def ensure_connection(conn_factory, conn):
    if conn is None or conn.closed != 0:
        return conn_factory()
    return conn


def register_invoice(barcode_list, client_nit, connection_db, conn_factory=None):
    if not barcode_list:
        print("Info: barcode_list vacío. Nada que procesar.")
        return False

    try:
        if conn_factory:
            connection_db = ensure_connection(conn_factory, connection_db)

        cursor = connection_db.cursor()

        # UUIDs y datos de la factura
        uuid_invoice = str(uuid.uuid4()).replace("-", "")[:32]
        uuid_client = get_uuid_client_by_nit(
            nit_client_search=client_nit,
            connection_db=connection_db,
        )
        if not uuid_client:
            raise ValueError("Cliente no encontrado")

        invoice_serial = f"AU-{random.randint(1000, 9999)}"
        date_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        checked_invoice = False

        # 1) Insertar factura
        cursor.execute(
            """
            INSERT INTO invoice (uuid, serial, date, checked)
            VALUES (%s, %s, %s, %s)
            """,
            (uuid_invoice, invoice_serial, date_now, checked_invoice),
        )

        # preparar placeholders para IN (...)
        placeholders = ",".join(["%s"] * len(barcode_list))

        # 2) Actualizar rolls
        update_sql = f"UPDATE roll SET checked = %s WHERE uuid IN ({placeholders})"
        cursor.execute(update_sql, tuple([True] + barcode_list))

        # 3) Insertar invoice_roll
        invoice_roll_records = [
            (str(uuid.uuid4()).replace("-", "")[:32], uuid_client, code)
            for code in barcode_list
        ]
        cursor.executemany(
            """
            INSERT INTO invoice_roll (uuid, uuid_client, uuid_roll)
            VALUES (%s, %s, %s)
            """,
            invoice_roll_records,
        )

        # 4) Traer info de los rolls
        select_sql = (
            f"SELECT uuid, roll, item, color, mts, kg, siigo_code, container "
            f"FROM roll WHERE uuid IN ({placeholders})"
        )
        cursor.execute(select_sql, tuple(barcode_list))
        list_rolls = _rows_to_dicts(cursor)

        connection_db.commit()

        # 5) Generar PDFs
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        create_non_group_invoice_pdf(
            client="",
            nit="",
            list_rolls=list_rolls,
            path_folder=downloads_path,
        )

        group_color = group_by_color(list_rolls=list_rolls)
        create_group_invoice_pdf(
            client="",
            client_nit="",
            color_group=group_color,
            path_folder=downloads_path,
            note_number=invoice_serial,
        )

        print("Info: Registro de factura [Completado]")
        return True

    except Exception as e:
        if connection_db and connection_db.closed == 0:
            try:
                connection_db.rollback()
            except Exception:
                pass

        # Guardar copia para reintentar
        failed_invoices.append({
            "barcode_list": list(barcode_list),
            "client_nit": client_nit,
        })

        print(f"Info: Registro de factura [Fallido]: {e}")
        print("Factura pendiente de reintento.")
        return False


def retry_failed(connection_db, conn_factory=None):
    global failed_invoices
    pendientes = failed_invoices[:]
    failed_invoices.clear()

    for inv in pendientes:
        ok = register_invoice(
            inv["barcode_list"],
            inv["client_nit"],
            connection_db,
            conn_factory=conn_factory,
        )
        if not ok:
            failed_invoices.append(inv)
