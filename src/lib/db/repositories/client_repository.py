def get_uuid_client_by_nit(nit_client_search, connection_db):
    try:
        cursor = connection_db.cursor()

        query = """
            SELECT uuid, name, address
            FROM client
            WHERE nit_client = %s
        """
        cursor.execute(query, (nit_client_search,))
        result = cursor.fetchone()

        cursor.close()

        if result:

            return result
        else:
            return None

    except Exception as e:
        print(f"Error al buscar el cliente con nit {nit_client_search}: {e}")
        return None
    
