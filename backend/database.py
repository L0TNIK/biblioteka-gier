# polaczenie z baza danych
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# bierze adres bazy z pliku .env zeby nie musiec przepisywac
load_dotenv("../.env")
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Brak DATABASE_URL w pliku .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# otwiera polaczenie z baza na czas zapytania i potem je zamyka
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()