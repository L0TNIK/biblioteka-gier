#jak schemat zwaliduje informacje to daje je do modelu
from sqlalchemy import Column, Integer, String
from database import Base

class Game(Base):
    __tablename__ = "gry"

    id = Column(Integer, primary_key=True)
    tytul = Column(String)
    ocena = Column(Integer)
    steam_appid = Column(Integer)
    image = Column(String)