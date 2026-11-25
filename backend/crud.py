#funkcje ktore dodam pozniej do endpointow (sluza one do gadania z baza danych)
import models

def GetUserByName(db, nazwa):
    return  db.query(models.User).filter(models.User.nazwa == nazwa).first()

def GetUserByEmail(db, email):
    return db.query(models.User).filter(models.User.email == email).first()

def GetUserById(db, userId):
    return db.query(models.User).filter(models.User.id == userId).first()

def CreateUser(db, nazwa, email, hasloHash):
    user = models.User(nazwa = nazwa, email=email, haslo_hash= hasloHash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def GetGames(db, userId, search=None, sort="asc"):
    query = db.query(models.Game).filter(models.Game.user_id == userId)
    if search:
        query = query.filter(models.Game.tytul.ilike(f"%{search}%"))
    if sort == "desc":
        query = query.order_by(models.Game.tytul.desc())
    else:
        query = query.order_by(models.Game.tytul.asc())
    return query.all()

def GetGame(db, gameId, userId):
    return db.query(models.Game).filter(
        models.Game.id == gameId, models.Game.user_id == userId
    ).first()

def CreateGame(db, game, userId):
    NewGame = models.Game(
        tytul=game.tytul,
        steam_appid=game.steam_appid,
        image=game.image,
        ocena=game.ocena,
        gatunek=game.gatunek,
        status=game.status,
        user_id=userId,
    )
    db.add(NewGame)
    db.commit()
    db.refresh(NewGame)
    return NewGame

def UpdateGame(db, gameId, game, userId):
    dbGame = GetGame(db, gameId, userId)
    if dbGame is None:
        return None

    dbGame.tytul = game.tytul
    dbGame.ocena = game.ocena
    dbGame.gatunek = game.gatunek
    dbGame.status = game.status

    db.commit()
    db.refresh(dbGame)
    return dbGame

def DeleteGame(db, gameId, userId):
    dbGame = GetGame(db, gameId, userId)
    if dbGame is None:
        return False
    db.delete(dbGame)
    db.commit()
    return True