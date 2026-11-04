from sqlalchemy import Column, Integer, String
from database import Base

class Game(Base):
    __tablename__ = "gry"

    id = Column(Integer, primary_key=True)
    tytul = Column(String)
    platforma = Column(String)
    ocena = Column(Integer)
    status = Column(String)