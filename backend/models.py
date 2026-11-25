from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


# opisuje tabele users w bazie (dane logowania kazdego uzytkownika)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    haslo_hash = Column(String, nullable=False)


# opisuje tabele gry w bazie (biblioteka gier przypisana do usera)
class Game(Base):
    __tablename__ = "gry"

    id = Column(Integer, primary_key=True)
    tytul = Column(String, nullable=False)
    steam_appid = Column(Integer)
    image = Column(String)
    ocena = Column(Integer)
    gatunek = Column(String)
    status = Column(String, default="Do ogrania", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)