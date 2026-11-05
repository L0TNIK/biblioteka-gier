#jak dane maja byc formatowane
from pydantic import BaseModel, ConfigDict


class GameCreate(BaseModel):
    tytul: str
    platforma: str | None = None
    ocena: int | None = None
    status: str = "do zagrania"

class GameOut(GameCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)#zmiana obiektu na JSON
    