from src.lib.db.db_connection import connection_db
from src.utils.handle_bd import get_list_import_rolls


conn = connection_db()

all_list_rolls =get_list_import_rolls(connection_db=conn)

data= {'data_container':{'itc-a4367-120': []}}
for roll in all_list_rolls:
    if roll["container"] == 'itc-a4367-120':
        data['data_container']['itc-a4367-120'].append(roll)


print(data)


