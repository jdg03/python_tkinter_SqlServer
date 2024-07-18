import pyodbc
from decouple import config

server = config('SERVER')
database = config('DATABASE')
username = config("USER")
password = config("PASSWORD")


connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};' \
                   f'UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'


def connect(connectionDBString):
    try:
        conn = pyodbc.connect(connectionDBString)
        return conn
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)


def create_table(table_name: str, columns: list[str], db_cursor):
    all_columns = ",\n\t".join(columns)
    sql_query = f"""CREATE TABLE {table_name}(   
                        {all_columns}
                    );
                    """
    db_cursor.execute(sql_query)

    db_cursor.commit()

    print(sql_query)


def insert_data(table_name, column_names, insert_values, db_cursor):
    columns_string = ", ".join(column_names)
    placeholders = ", ".join(["?" for _ in insert_values])

    sql_query = f"INSERT INTO {table_name} ({columns_string}) VALUES({placeholders})"

    db_cursor.execute(sql_query, insert_values)
    db_cursor.commit()

    print(sql_query + f"\nvalues: {insert_values}")


def update_data(table_name, colum_names, insert_values, db_cursor):
    for i, col in enumerate(colum_names):
        colum_names[i] = col + "=?"
    colum_string = ", ".join(colum_names)
    sql_query = f"UPDATE {table_name} SET {colum_string} WHERE ID=?"

    db_cursor.execute(sql_query, insert_values)
    db_cursor.commit()


def delete_data(table_name: str, del_id, db_cursor):
    sql_query =f"DELETE FROM {table_name} WHERE ID={del_id}"
    db_cursor.execute(sql_query)
    db_cursor.commit()


def get_all_data(database_name, db_cursor):
    sql_query = f"SELECT * FROM {database_name}"

    db_cursor.execute(sql_query)

    rows = db_cursor.fetchall()

    return rows


def get_all_tables(db_cursor):
    sql_query= """
        SELECT name
        FROM sys.tables;
    """

    db_cursor.execute(sql_query)
    rows = db_cursor.fetchall()

    table_names = [row[0] for row in rows]

    return table_names


def delete_database(table_name, db_cursor):
    sql_query = f"DROP TABLE {table_name}"
    db_cursor.execute(sql_query)
    db_cursor.commit()


if __name__ == "__main__":
    print("Start")
    con= connect(connectionString)

    cursor = con.cursor()

    columns = ["Id INTEGER PRIMARY KEY", "Codigo VARCHAR(10) NOT NULL UNIQUE", "Nombre VARCHAR(200) NOT NULL UNIQUE"]

    columns2 = ["Id", "Codigo", "Nombre"]
    values = [2, "Man", "Mantenimiento"]

    table_countries = ["ID INT PRIMARY KEY IDENTITY(1,1)","ISO3 VARCHAR(5)", "CountryName VARCHAR(50)", "Capital VARCHAR(50)", "CurrencyCode VARCHAR(30)"]

    rows = get_all_tables(cursor)

    for row in rows:
        print(row)

