import uuid

def insert_invoice_rolls(cursor, uuid_client, barcode_list, uuid_invoice):
    records = [
        (str(uuid.uuid4()).replace("-", "")[:32], uuid_client, code, uuid_invoice)
        for code in barcode_list
    ]
    cursor.executemany(
        """
        INSERT INTO invoice_roll (uuid, uuid_client, uuid_roll, uuid_invoice)
        VALUES (%s, %s, %s, %s)
        """,
        records,
    )
