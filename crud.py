from sqlalchemy.orm import Session

import models, schemas

def get_game(db: Session, room_id: int):
    return db.query(models.Game).filter(models.Game.rmid == room_id).first()

def create_game(db: Session, room_id: int, rolesinit: str):
    game_obj = models.Game(rmid=room_id, rolesinit=rolesinit, rolesingame=rolesinit)
    db.add(game_obj)
    db.commit()
    db.refresh(game_obj)
    return game_obj

def delete_room(db: Session, room_id: int):
    db.query(models.Game).filter(models.Game.rmid == room_id).delete()
    db.query(models.Player).filter(models.Player.rmid == room_id).delete()
    db.commit()
    return {'Result': 'delete room'}

def get_player_by_room_pos_name(db: Session, rm: int, pos: int, name: str):
    return db.query(models.Player).filter(models.Player.rmid == rm).filter(models.Player.pos == pos).filter(models.Player.name == name).first()

def get_all_players_by_room(db: Session, rm: int):
    return db.query(models.Player).filter(models.Player.rmid == rm).all()

def create_player(db: Session, room_id: int, pos: int, name: str):
    player_obj = models.Player(rmid=room_id, pos=pos, name=name, op1=-1, op2=-1, awaken=-1, voted=-1)
    db.add(player_obj)
    db.commit()
    db.refresh(player_obj)
    return player_obj

def delete_players_by_room(db: Session, room_id: int):
    db.query(models.Player).filter(models.Player.rmid == room_id).delete()
    return {'Result': 'delete all players in the room'}

# def get_items(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # db_item = models.Item(**item.dict(), owner_id=user_id)
    # db.add(db_item)
    # db.commit()
    # db.refresh(db_item)
    # return db_item
