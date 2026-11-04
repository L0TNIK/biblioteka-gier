import models

def GetGames(db):
    return db.query(models.Game).all()

def GetGame(db):
    return db.query(models.Game).filter(models.Game.id == gameId).first()

def CreateGame(db, game):
    NewGame = models.Game(
    tytul=game.tytul,
    platforma=game.platforma,
    ocena=game.ocena,
    status=game.status,
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
    dbGame.platforma = game.platforma
    dbGame.ocena = game.ocena
    dbGame.status = game.status

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