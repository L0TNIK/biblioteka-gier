import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash

import crud
from database import get_db

load_dotenv("../.env")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Brak SECRET_KEY w pliku .env")

ALGORITHM = "HS256"
WAZNOSC_MINUT = 60 * 24

hasher = PasswordHash.recommended()
bearer = HTTPBearer()

def hashuj_haslo(haslo):
    return hasher.hash(haslo)

def sprawdz_haslo(haslo, haslo_hash):
    return hasher.verify(haslo,haslo_hash)

def stworz_token(user_id):
    wygasa = datetime.now(timezone.utc) + timedelta(minutes=WAZNOSC_MINUT)
    return jwt.encode({"sub": str(user_id), "exp": wygasa}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(dane: HTTPAuthorizationCredentials = Depends(bearer), db=Depends(get_db)):
    blad = HTTPException(status_code=401, detail="Zaloguj się ponownie")
    try:
        payload = jwt.decode(dane.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise blad

    user = crud.GetUserById(db, user_id)
    if user is None:
        raise blad
    return user