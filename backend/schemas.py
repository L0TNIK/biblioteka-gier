from pydantic import BaseModel, ConfigDict, Field


# sprawdza dane przy dodawaniu albo edytowaniu gry
class GameCreate(BaseModel):
    tytul: str = Field(min_length=1, max_length=150)
    ocena: int | None = None
    steam_appid: int | None = None
    image: str | None = None
    gatunek: str | None = Field(default=None, max_length=30)
    status: str = Field(default="Do ogrania", max_length=30)


# format danych gry ktory backend odsyla na strone (dorzuca id z bazy)
class GameOut(GameCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# sprawdza dane przy rejestracji (dlugosc nicku, hasla i poprawny mail)
class UserCreate(BaseModel):
    nazwa: str = Field(min_length=3, max_length=30)
    email: str = Field(max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    haslo: str = Field(min_length=8, max_length=64)


# sprawdza dane przy logowaniu (nick albo mail + haslo)
class UserLogin(BaseModel):
    nazwa: str
    haslo: str


# format tokena zwracanego po udanym logowaniu lub rejestracji
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"