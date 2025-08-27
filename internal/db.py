from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
get_db = contextmanager(get_session)
