#jak dane maja byc formatowane
from pydantic import BaseModel, ConfigDict


class GameCreate(BaseModel):
    tytul: str
    ocena: int | None = None
    steam_appid: int | None = None
    image: str | None = None

class GameOut(GameCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)#zmiana obiektu na JSON
    