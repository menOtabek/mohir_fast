from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:1211@localhost/mohir_fast"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
session = sessionmaker(bind=engine)
