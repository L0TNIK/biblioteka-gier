#jak schemat zwaliduje informacje to daje je do modelu
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Game(Base):
    __tablename__ = "gry"

    id = Column(Integer, primary_key=True)
    tytul = Column(String)
    ocena = Column(Integer)
    steam_appid = Column(Integer)
    image = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    haslo_hash = Column(String, nullable=False)