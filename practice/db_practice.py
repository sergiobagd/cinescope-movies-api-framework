import psycopg2

def connect_to_postgres():
    """
    Function for connection to PostgreSQL DB
    """
    connection = None
    cursor = None
    try:
        # Connection with PostgreSQL
        connection = psycopg2.connect(
            dbname="testdb",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )

        print("Connection was successfully created!")

        # Creating a cursor
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Print info about PostgreSQL server
        print("Information about PostgreSQL server:")
        print(connection.get_dsn_parameters(), "\n")

        # Executing SQL request
        cursor.execute("SELECT version();")

        # Getting result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except Exception as error:
        print("Error while working with PostgreSQL", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection with PostgreSQL is closed.")


connect_to_postgres()

# try:
#     cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
#     raise ValueError("Error while executing request") # Imitation of error
#     connection.commit() # Commiting changes to DB by real
# except Exception as e:
#     print(f"Error occured: {e}")
#     connection.rollback() # Cancelling our changes in DB

# # Using context managers
# with psycopg2.connect(dbname="test_db", user="user", password="password") as connection:
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM users")
#         print(cursor.fetchall())
# # Connection and cursor will automatically close after quitting this block of context manager "with"
#
# # Autocommit
#
# connection.autocommit = True
# cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ("Charlie", "charlie@example.com"))
# # Changes will automatically be saved in DB without adding command commit()

# Isolations - how transactions interact with each other
# connection.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
# ISOLATION_LEVEL_SERIALIZABLE: Самый строгий уровень, гарантирующий последовательное выполнение транзакций.

# Parameters of DB in a dict format
# params = connection.get_dsn_parameters()
# print(f"Connected to {params["dbname"]} on {params["host"]}")

# Notifications from PostgreSQL server "notices"
# for notice in connection.notices:
#     print(f"Notification: {notice}")

# try:
#     cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (1, "John"))
#     connection.commit()
#
# except psycopg2.IntegrityError as e:
#     print(f"Error of data integrity: {e}")
#     connection.rollback()
#
# except psycopg2.OperationalError as e:
#     print(f"Error of connection: {e}")
#     # Trying to reconnect
#
# except psycopg2.ProgrammingError as e:
#     print(f"Error of SQL code: {e}")
#     connection.rollback()

# 1. Standard Cursor - returns Tuples
cursor = connection.cursor()

cursor.execute("SELECT id, name, age FROM users")
row = cursor.fetchone()
# # row будет в виде: (1, 'Иван', 30) - Tuple

# 2. DictCursor - returns dicts, but saves indexes

dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

dict_cursor.execute("SELECT id, name, age FROM users")
row = dict_cursor.fetchone()

# Access like dict
print(row["name"]) # 'Иван'
# Access like list
print(row[1]) # 'Иван'

# RealDictCursor - returns real dicts (without indexes)

real_dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
real_dict_cursor.execute("SELECT id, name, age FROM users")
row = real_dict_cursor.fetchone()
print(row["name"]) # 'Иван'
# row[1] вызовет ошибку

# NamedTupleCursor

named_tuple_cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
named_tuple_cursor.execute("SELECT id, name, age FROM users")
row = named_tuple_cursor.fetchone()
print(row.name) # 'Иван'
# Доступ как к индексам также работает
print(row[1])# 'Иван'

# NamedCursor (for thread processing of big data sets)
named_cursor = connection.cursor(name="my_cursor")

named_cursor.execute("SELECT id, name, age FROM users")
while True:
    rows = named_cursor.fetchmany(size=100) # Get next 100 rows
    if not rows:
        break
    for row in rows:
        print(row) # Processing each row


cursor.execute("SELECT id, name FROM users")

# Получение первой строки
first_row = cursor.fetchone()
if first_row:
    print(f"ID: {first_row[0]}, Name: {first_row[1]}")

# Получение следующей строки
second_row = cursor.fetchone()
if second_row:
    print(f"ID: {second_row[0]}, Name: {second_row[1]}")

cursor.execute("SELECT id, name FROM users")

# Получение всех строк сразу
all_rows = cursor.fetchall()
for row in all_rows:
    print(f"ID: {row[0]}, Name: {row[1]}")

cursor.execute("SELECT id, name FROM users")

# Получение пакета из 5 строк
batch = cursor.fetchmany(5)
for row in batch:
    print(f"ID: {row[0]}, Name: {row[1]}")

# Получение следующего пакета
next_batch = cursor.fetchmany(5)




