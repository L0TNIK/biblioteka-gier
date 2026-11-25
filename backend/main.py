# endpointy
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


# zwraca nick aktualnie zalogowanego usera
@app.get("/ja")
def me(user=Depends(get_current_user)):
    return {"nazwa": user.nazwa}


# zaklada nowe konto i od razu zwraca token do zalogowania
@app.post("/rejestracja", response_model=schemas.Token)
def register(dane: schemas.UserCreate, db=Depends(get_db)):
    email = dane.email.strip().lower()
    if crud.GetUserByName(db, dane.nazwa):
        raise HTTPException(status_code=400, detail="taka nazwa uzytkownika juz istnieje")
    if crud.GetUserByEmail(db, email):
        raise HTTPException(status_code=400, detail="Konto z tym adresem e-mail już istnieje")
    user = crud.CreateUser(db, dane.nazwa, email, hashuj_haslo(dane.haslo))
    return {"access_token": stworz_token(user.id), "token_type": "bearer"}


# loguje usera po nicku albo mailu i daje mu token
@app.post("/logowanie", response_model=schemas.Token)
def login(dane: schemas.UserLogin, db=Depends(get_db)):
    login_input = dane.nazwa.strip()
    if "@" in login_input:
        user = crud.GetUserByEmail(db, login_input.lower())
    else:
        user = crud.GetUserByName(db, login_input)
    if user is None or not sprawdz_haslo(dane.haslo, user.haslo_hash):
        raise HTTPException(status_code=401, detail="Zły login lub hasło")
    return {"access_token": stworz_token(user.id), "token_type": "bearer"}


# pobiera liste wszystkich gier zalogowanego usera
@app.get("/gry", response_model=list[schemas.GameOut])
def list_games(search: str | None = None, sort: str = "asc",
               db=Depends(get_db), user=Depends(get_current_user)):
    return crud.GetGames(db, user.id, search, sort)


# pobiera szczegoly jednej konkretnej gry
@app.get("/gry/{gameId}", response_model=schemas.GameOut)
def read_game(gameId: int, db=Depends(get_db), user=Depends(get_current_user)):
    game = crud.GetGame(db, gameId, user.id)
    if game is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return game


# dodaje nowa gre do biblioteki usera
@app.post("/gry", response_model=schemas.GameOut)
def add_game(game: schemas.GameCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return crud.CreateGame(db, game, user.id)


# aktualizuje dane wybranej gry
@app.put("/gry/{gameId}", response_model=schemas.GameOut)
def edit_game(gameId: int, game: schemas.GameCreate,
              db=Depends(get_db), user=Depends(get_current_user)):
    updated = crud.UpdateGame(db, gameId, game, user.id)
    if updated is None:
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return updated


# usuwa wybrana gre z biblioteki
@app.delete("/gry/{gameId}")
def remove_game(gameId: int, db=Depends(get_db), user=Depends(get_current_user)):
    if not crud.DeleteGame(db, gameId, user.id):
        raise HTTPException(status_code=404, detail="nie ma takiej gry")
    return {"message": "usunieto"}


# szuka gier w sklepie steam po wpisanej nazwie
@app.get("/steam/search")
def steam_search(term: str):
    try:
        return steam.SearchSteam(term)
    except Exception:
        raise HTTPException(status_code=502, detail="steam nie odpowiada")


# pobiera dokladne info o grze ze steama (okladka, gatunek) po jej id
@app.get("/steam/details/{appId}")
def steam_details(appId: int):
    try:
        return steam.GetSteamDetails(appId)
    except Exception as e:
        print("BLAD DETAILS:", repr(e))
        raise HTTPException(status_code=502, detail="nie udalo sie pobrac danych ze steama")