#funkcje ktore dodam pozniej do endpointow (sluza one do gadania z baza danych)
import models

def GetGames(db):
    return db.query(models.Game).all()

def GetGame(db,gameId):
    return db.query(models.Game).filter(models.Game.id == gameId).first()

def CreateGame(db, game):
    NewGame = models.Game(
    tytul=game.tytul,
    ocena=game.ocena,
    steam_appid=game.steam_appid,
    image=game.image,
    )
    db.add(NewGame)
    db.commit()
    db.refresh(NewGame)
    return NewGame

def UpdateGame(db, gameId, game):
    dbGame = GetGame(db,gameId)
    if dbGame is None:
        return None

    dbGame.tytul = game.tytul
    dbGame.ocena = game.ocena

    db.commit()
    db.refresh(dbGame)
    return dbGame

def DeleteGame(db, GameId):
    dbGame = GetGame(db,GameId)
    if dbGame is None:
        return False
    db.delete(dbGame)
    db.commit()
    return True

def GetGames(db, search=None, sort="asc"):
    query = db.query(models.Game)
    if search:
        query = query.filter(models.Game.tytul.ilike(f"{search}%"))
    if sort == "desc":
        query = query.order_by(models.Game.tytul.desc())
    else:
        query = query.order_by(models.Game.tytul.asc())
    return query.all()