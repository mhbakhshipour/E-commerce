import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv("e_commerce/.env")

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    os.environ["DATABASE_USER"],
    os.environ["DATABASE_PASSWORD"],
    os.environ["DATABASE_HOST"],
    os.environ["DATABASE_PORT"],
    os.environ["DATABASE_DB"],
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
