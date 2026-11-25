# funkcje ktore dodam pozniej do endpointow (sluza one do gadania z baza danych)
import models


# szuka usera w bazie po nicku
def GetUserByName(db, nazwa):
    return db.query(models.User).filter(models.User.nazwa == nazwa).first()


# szuka usera w bazie po mailu
def GetUserByEmail(db, email):
    return db.query(models.User).filter(models.User.email == email).first()


# szuka usera w bazie po jego id
def GetUserById(db, userId):
    return db.query(models.User).filter(models.User.id == userId).first()


# zapisuje nowego usera w bazie
def CreateUser(db, nazwa, email, hasloHash):
    user = models.User(nazwa=nazwa, email=email, haslo_hash=hasloHash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# pobiera wszystkie gry danego usera (z opcja szukania po tytule i sortowania)
def GetGames(db, userId, search=None, sort="asc"):
    query = db.query(models.Game).filter(models.Game.user_id == userId)
    if search:
        query = query.filter(models.Game.tytul.ilike(f"%{search}%"))
    if sort == "desc":
        query = query.order_by(models.Game.tytul.desc())
    else:
        query = query.order_by(models.Game.tytul.asc())
    return query.all()


# wyciaga jedna konkretna gre nalezaca do tego usera
def GetGame(db, gameId, userId):
    return db.query(models.Game).filter(
        models.Game.id == gameId, models.Game.user_id == userId
    ).first()


# dodaje nowa gre do bazy i przypisuje ja do usera
def CreateGame(db, game, userId):
    new_game = models.Game(
        tytul=game.tytul,
        steam_appid=game.steam_appid,
        image=game.image,
        ocena=game.ocena,
        gatunek=game.gatunek,
        status=game.status,
        user_id=userId,
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


# nadpisuje dane istniejacej gry w bazie
def UpdateGame(db, gameId, game, userId):
    db_game = GetGame(db, gameId, userId)
    if db_game is None:
        return None

    db_game.tytul = game.tytul
    db_game.ocena = game.ocena
    db_game.gatunek = game.gatunek
    db_game.status = game.status

    db.commit()
    db.refresh(db_game)
    return db_game


# wywala gre z bazy jesli nalezy do tego usera
def DeleteGame(db, gameId, userId):
    db_game = GetGame(db, gameId, userId)
    if db_game is None:
        return False
    db.delete(db_game)
    db.commit()
    return True