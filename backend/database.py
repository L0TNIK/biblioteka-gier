import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#bierze baze z pliku .env zeby nie musiec przepisywac
load_dotenv("../.env")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#otwiera i zamyka sesje automatycznie
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()