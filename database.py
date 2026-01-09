import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_db_engine():
    # Built-in SQLAlchemy engine handles the connection pooling and dialect
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(url)