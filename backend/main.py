#endpointy
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
import models, schemas, crud, steam

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def aga():
    return {"wiadomosc": "aga"}

@app.get("/gry", response_model=list[schemas.GameOut])
def ListGames(db=Depends(get_db)):
    return crud.GetGames(db)

@app.get("/gry/{gameId}", response_model=schemas.GameOut)
def ReadGame(gameId: int, db=Depends(get_db)):
    game = crud.GetGame(db, gameId)
    if game is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return game

@app.post("/gry", response_model=schemas.GameOut)
def AddGame(game: schemas.GameCreate, db=Depends(get_db)):
    return crud.CreateGame(db, game)

@app.put("/gry/{gameId}", response_model=schemas.GameOut)
def EditGame(gameId: int, game: schemas.GameCreate, db=Depends(get_db)):
    updated = crud.UpdateGame(db, gameId, game)
    if updated is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return updated

@app.delete("/gry/{gameId}")
def RemoveGame(gameId: int, db=Depends(get_db)):
    if not crud.DeleteGame(db, gameId):
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return {"message": "usunieto"}

@app.get("/gry", response_model=list[schemas.GameOut])
def ListGames(search: str | None = None, sort: str = "asc", db=Depends(get_db)):
    return crud.GetGames(db,search, sort)

@app.get("/steam/search")
def SteamSearch(term: str):
    try:
        return steam.SearchSteam(term)
    except Exception:
        raise HTTPException(status_code=502, detail="steam nie odpowiada")