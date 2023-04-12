import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_HOST=os.environ.get('DB_HOST', "localhost")
DB_PORT=os.environ.get('DB_PORT', "3306")
DB_NAME=os.environ.get('DB_NAME', "waste_segragation")
DB_USER=os.environ.get('DB_USER', "admin")
DB_PASSWORD=os.environ.get('DB_PASSWORD', "admin#123")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" 
SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_size=10,
    max_overflow=20,
    # connect_args={"check_same_thread": False}  # only if sqlite is used
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
