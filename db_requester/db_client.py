from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DataBaseCreds
USERNAME = DataBaseCreds.USERNAME
PASSWORD = DataBaseCreds.PASSWORD
HOST = DataBaseCreds.HOST
PORT = DataBaseCreds.PORT
DATABASE_NAME = DataBaseCreds.NAME

# Engine to connect to DB
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False # Set True for debugging SQL requests
)

# Create sessions fabric
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Creates new DB session
    """
    return SessionLocal()








# def connect_to_db_movies_postgresql():
#     connection = None
#     # cursor = None
#
#     try:
#         connection = psycopg2.connect(
#             dbname=DataBaseCreds.NAME,
#             user=DataBaseCreds.USERNAME,
#             password=DataBaseCreds.PASSWORD,
#             host=DataBaseCreds.HOST,
#             port=DataBaseCreds.PORT
#         )
#
#         server_info = connection.get_dsn_parameters()
#         print(f"Info about {DataBaseCreds.NAME} DB server: \n"
#               f"{server_info}")
#
#         cursor = connection.cursor(cursor_factory=DictCursor)
#         # cursor.execute(f'''
#         # SELECT * FROM genres
#         # ORDER BY id DESC LIMIT 100''')
#         # record = cursor.fetchall()
#         # print(record)
#         # movie_id = "4"
#         cursor.execute("""
#         SELECT * from users
#         WHERE id = %s
#         """, ("995c7fa5-34b3-4f48-93a6-ffbf7b6dd360",))
#         record = cursor.fetchall()
#         print(record)
#         # cursor.execute("SELECT * FROM movies WHERE movies.id = %s", (movie_id))
#         # record = cursor.fetchall()
#         # print(record)
#         # genre_id = "3"
#         # price = "200"
#         # cursor.execute(f"""
#         # SELECT id, name, price, genre_id FROM movies
#         # WHERE movies.genre_id = %(genre)s
#         # AND movies.price < %(price)s LIMIT 10""", {"genre": genre_id, "price": price})
#         # record = cursor.fetchall()
#         # for row in record:
#         #     print(f"""
#         #     ID: {row[0]}
#         #     NAME: {row[1]}
#         #     PRICE: {row[2]}
#         #     GENRE_ID: {row[3]}""")
#         # cursor.execute("""
#         # INSERT INTO genres (name) VALUES (%s) RETURNING id""", ("Психологический ботано-хоррор",))
#         # new_id = cursor.fetchone()[0]
#         # print(f"New entry was created with ID: {new_id}")
#         # connection.commit()
#
#         # cursor.execute("""
#         # UPDATE genres
#         # SET name = %(new_name)s
#         # WHERE id = %(id)s;
#         # """, ({"new_name": "Нереалистичный ботано-хоррор", "id": "84"}))
#         # affected_rows = cursor.rowcount
#         # print(f"Quantity of updated rows: {affected_rows}")
#         # connection.commit()
#
#         # cursor.execute("""
#         # DELETE FROM genres
#         # WHERE name = %s;
#         # """, ("Нереалистичный ботано-хоррор",)
#         # )
#         # affected_rows = cursor.rowcount
#         # print(f"Quantity of deleted rows: {affected_rows}")
#         # connection.commit()
#
#
#
#     except psycopg2.OperationalError as e:
#         print(f"Connection error: {e}")
#
# connect_to_db_movies_postgresql()
