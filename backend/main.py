#endpointy
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
import models, schemas, crud, steam
from auth import hashuj_haslo, sprawdz_haslo, stworz_token, get_current_user

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

@app.post("/rejestracja", response_model=schemas.Token)
def Register(dane: schemas.UserCreate, db=Depends(get_db)):
    email = dane.email.strip().lower()
    if crud.GetUserByName(db, dane.nazwa):
        raise HTTPException(status_code=400, detail="taka nazwa uzytkownika juz istnieje")
    if crud.GetUserByEmail(db, email):
        raise HTTPException(status_code=400, detail="Konto z tym adresem e-mail już istnieje")
    user = crud.CreateUser(db, dane.nazwa, email, hashuj_haslo(dane.haslo))
    return {"access_token": stworz_token(user.id), "token_type": "bearer"}

@app.post("/logowanie", response_model=schemas.Token)
def Login(dane: schemas.UserLogin, db=Depends(get_db)):
    login = dane.nazwa.strip()
    if "@" in login:
        user = crud.GetUserByEmail(db, login.lower())
    else:
        user = crud.GetUserByName(db, login)
    if user is None or not sprawdz_haslo(dane.haslo, user.haslo_hash):
        raise HTTPException(status_code=401, detail="Zły login lub hasło")
    return {"access_token": stworz_token(user.id), "token_type": "bearer"}

@app.get("/gry", response_model=list[schemas.GameOut])
def ListGames(search: str | None = None, sort: str = "asc",
              db=Depends(get_db), user=Depends(get_current_user)):
    return crud.GetGames(db, user.id, search, sort)

@app.get("/gry/{gameId}", response_model=schemas.GameOut)
def ReadGame(gameId: int, db=Depends(get_db), user=Depends(get_current_user)):
    game = crud.GetGame(db, gameId, user.id)
    if game is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return game

@app.post("/gry", response_model=schemas.GameOut)
def AddGame(game: schemas.GameCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return crud.CreateGame(db, game, user.id)

@app.put("/gry/{gameId}", response_model=schemas.GameOut)
def EditGame(gameId: int, game: schemas.GameCreate,
             db=Depends(get_db), user=Depends(get_current_user)):
    updated = crud.UpdateGame(db, gameId, game, user.id)
    if updated is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return updated

@app.delete("/gry/{gameId}")
def RemoveGame(gameId: int, db=Depends(get_db), user=Depends(get_current_user)):
    if not crud.DeleteGame(db, gameId, user.id):
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return {"message": "usunieto"}

@app.get("/steam/search")
def SteamSearch(term: str):
    try:
        return steam.SearchSteam(term)
    except Exception:
        raise HTTPException(status_code=502, detail="steam nie odpowiada")

@app.get("/steam/details/{appId}")
def steam_details(appId: int):
    try:
        return steam.GetSteamDetails(appId)
    except Exception as e:
        print("BLAD DETAILS:", repr(e))
        raise HTTPException(status_code=502, detail=repr(e))