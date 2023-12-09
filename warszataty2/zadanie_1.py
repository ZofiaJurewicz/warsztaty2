from psycopg2 import connect, OperationalError, sql, DatabaseError

try:
    cnx = connect(
        user='postgres',
        password='coderslab',
        host='localhost',
        port='5432',
        database='create_db'
    )
    cursor = cnx.cursor()
    print('Connected')
except OperationalError as error:
    print('Conection error')
    raise ValueError(f'Conection error: {error}')

try:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('create_db')))
except (OperationalError, DatabaseError) as error:
    print(f'Error creating database {error}')



query_create_tb_user = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL, 
        username VARCHAR(255),
        password VARCHAR(80) DEFAULT 'ala',
        PRIMARY KEY (id)
        )
""").format(table_name=sql.Identifier('User'))

query_create_tb_messages = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        text VARCHAR(255),
        last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        from_id INTEGER REFERENCES {table_name_foreign}(id),
        to_id INTEGER REFERENCES {table_name_foreign}(id) 
    )
""").format(
    table_name=sql.Identifier('Messages'),
    table_name_foreign=sql.Identifier('User')
)

with cnx:
    try:
        cursor.execute(query_create_tb_user)
    except DatabaseError as error:
        print(error)
cnx.commit()
cursor.close()
cnx.close()