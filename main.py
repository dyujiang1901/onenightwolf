from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from database import SessionLocal, engine

from schemas import *
import models, crud

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI(title="one night wolf",
              )

# 设置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/onenightwolf/playground/create/room/{rm_id}/ri/{role_init}")
def create_game(rm_id: int, role_init: str, db: Session = Depends(get_db)):
    game = crud.get_game(db, rm_id)
    if game:
        raise HTTPException(status_code=400, detail="room taken")
    return crud.create_game(db, rm_id, role_init)

@app.post("/onenightwolf/playground/delete/room/{rm_id}")
def delete_game(rm_id: int, db: Session = Depends(get_db)):
    return crud.delete_room(db, rm_id)

@app.get("/onenightwolf/playground/search/room/{rm_id}")
def get_game(rm_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, rm_id)
    if game is None:
        raise HTTPException(status_code=404, detail="game not found")
    return game

@app.post("/onenightwolf/prepare/create/room/{rm_id}/pos/{pos}/name/{username}")
def create_player(rm_id: int, pos: int, username: str, db: Session = Depends(get_db)):
    player = crud.get_player_by_room_pos_name(db, rm_id, pos, username)
    if player:
        raise HTTPException(status_code=400, detail="position taken")
    return crud.create_player(db, rm_id, pos, username)

@app.get("/onenightwolf/prepare/search/room/{rm_id}/pos/{pos}/name/{username}")
def get_player(rm_id: int, pos: int, username: str, db: Session = Depends(get_db)):
    player = crud.get_player_by_room_pos_name(db, rm_id, pos, username)
    if player is None:
        raise HTTPException(status_code=404, detail="No such player")
    return player
