#jak dane maja byc formatowane
from pydantic import BaseModel, ConfigDict, Field


class GameCreate(BaseModel):
    tytul: str
    ocena: int | None = None
    steam_appid: int | None = None
    image: str | None = None
    gatunek: str | None = Field(default=None, max_length=30)

class GameOut(GameCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)#zmiana obiektu na JSON

class UserCreate(BaseModel):
    nazwa: str = Field(min_length=3,max_length=30)
    email: str = Field(max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    haslo: str = Field(min_length=8, max_length=64)

class UserLogin(BaseModel):
    nazwa: str
    haslo: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
