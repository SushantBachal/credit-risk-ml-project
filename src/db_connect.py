import os
from dotenv import load_dotenv
import pymysql 
import urllib.parse
from sqlalchemy import create_engine

load_dotenv()
def get_db_engine():
    """
    Creates and returns a SQLAlchemy database engine.
    """
    # Database connection parameters
    username = "root"
    password = urllib.parse.quote_plus(os.getenv("DB_password"))
    host = "127.0.0.1"
    port = os.getenv("DB_port")
    database_name = "creditcarddb"

    # Create the database engine

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}")

    return engine   