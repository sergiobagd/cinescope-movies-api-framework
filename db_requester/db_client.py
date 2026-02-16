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