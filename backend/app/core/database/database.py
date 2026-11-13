from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

class Base(DeclarativeBase):
    pass

engine = create_engine( DB_URL )

LocalSession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()