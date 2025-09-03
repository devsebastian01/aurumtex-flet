import psycopg2

import psycopg2

def connection_db():
    try:
        conn = psycopg2.connect(
            host="dpg-d2oq36i4d50c73a8iipg-a.oregon-postgres.render.com",
            database="inventory_4hrp",
            user="aurumtex",
            password="2goEFIso3C6Eqrb3TNyGudHskcWpgXVM",
            port=5432,
            sslmode="require"
        )
        print("Info: Conexión a base de datos [Completado]")
        return conn
    except Exception as e:
        print("Info: Conexión a base de datos [Fallido]", e)

    
    