import os
import uuid
import random
from datetime import datetime

from src.lib.db.repositories.client_repository import get_uuid_client_by_nit
from src.utils.create_pdf import create_non_group_invoice_pdf, create_group_invoice_pdf
from src.utils.group_rolls import group_by_color

from src.lib.db.repositories.invoice_repository import insert_invoice
from src.lib.db.repositories.invoice_roll_repository import insert_invoice_rolls
from src.lib.db.repositories.roll_repository import update_rolls_checked, select_rolls_by_uuid
from src.utils.get_serial_invoice import get_and_increment_invoice_serial

# Cola global para facturas que fallaron
failed_invoices = []


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

        # Datos de la factura
        info_client = get_uuid_client_by_nit(
            nit_client_search=client_nit,
            connection_db=connection_db,
        )
        if not info_client:
            raise ValueError("Cliente no encontrado")

        invoice_serial = f"AU-{get_and_increment_invoice_serial()}"
        date_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        checked_invoice = False

        # 1) Insertar factura
        uuid_invoice = insert_invoice(cursor, invoice_serial, date_now, checked_invoice)

        # 2) Actualizar rolls
        update_rolls_checked(cursor, barcode_list, checked=True)

        
        # 3) Insertar invoice_roll
        uuid_client = info_client[0]
        insert_invoice_rolls(cursor, uuid_client, barcode_list, uuid_invoice)

        # 4) Traer info de los rolls
        list_rolls = select_rolls_by_uuid(cursor, barcode_list)

        connection_db.commit()

        # 5) Generar PDFs
        
        name_client = info_client[1]
        address_client = info_client[2]
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        create_non_group_invoice_pdf(
            nit="",
            client=name_client,
            list_rolls=list_rolls,
            path_folder=downloads_path,
        )

        group_color = group_by_color(list_rolls=list_rolls)
        create_group_invoice_pdf(
            address= address_client,
            client= name_client,
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
