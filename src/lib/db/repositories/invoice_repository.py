import uuid

def insert_invoice(cursor, serial, date_now, checked):
    uuid_invoice = str(uuid.uuid4()).replace("-", "")[:32]
    cursor.execute(
        """
        INSERT INTO invoice (uuid, serial, date, checked)
        VALUES (%s, %s, %s, %s)
        """,
        (uuid_invoice, serial, date_now, checked),
    )
    return uuid_invoice
