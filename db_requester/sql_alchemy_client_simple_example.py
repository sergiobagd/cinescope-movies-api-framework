from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from resources.db_creds import DataBaseCreds

# Connection to DB
host = DataBaseCreds.HOST
port = DataBaseCreds.PORT
database_name = DataBaseCreds.NAME
username = DataBaseCreds.USERNAME
password = DataBaseCreds.PASSWORD

# Create URL to connect DB
connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"

# Object for connection to DB
engine = create_engine(connection_string)

def sql_aclhemy_SQL():
    query = """
    SELECT id, email, full_name, "password", created_at, updated_at, verified, banned, roles
    FROM public.users
    WHERE id = :user_id
    """

    # Params for out SQL query request
    user_id = "995c7fa5-34b3-4f48-93a6-ffbf7b6dd360"

    # Execute our SQL query request
    with engine.connect() as connection: # Connect to DB and automatically close it after finishing
        result = connection.execute(text(query), {"user_id": user_id})
        for row in result:
            print(row)


sql_aclhemy_SQL()

def sql_alchemy_ORM():
    # Basic class for models
    Base = declarative_base()

    # Model of table "users"
    class User(Base):
        __tablename__ = "users"
        id = Column(String, primary_key=True)
        email = Column(String)
        full_name = Column(String)
        password = Column(String)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)
        verified = Column(Boolean)
        banned = Column(Boolean)
        roles = Column(String)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    user_id = "995c7fa5-34b3-4f48-93a6-ffbf7b6dd360"

    # Executing request
    user = session.query(User).filter(User.id == user_id).first()

    # Print result (we got object instead of just string now!)
    if user:
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Full name: {user.full_name}")
        print(f"Password: {user.password}")
        print(f"Created at: {user.created_at}")
        print(f"Updated at: {user.updated_at}")
        print(f"Verified: {user.verified}")
        print(f"Banned: {user.banned}")
        print(f"Roles: {user.roles}")
    else:
        print("User was not found.")

sql_alchemy_ORM()