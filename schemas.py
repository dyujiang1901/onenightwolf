from datetime import datetime

from fastapi import Body
from pydantic import BaseModel

from typing import List


class GameBase(BaseModel):
    rmid: int
    rolesinit: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    rolesingame: str

    class Config:
        orm_mode = True

class PlayerBase(BaseModel):
    rmid: int
    pos: int
    name: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    op1: int
    op2: int
    awaken: int
    voted: int
    id: int = None

    class Config:
        orm_mode = True

# class Response200(BaseModel):
    # code: int = 200
    # msg: str = "操作成功"
    # data: Message = None


# class ResponseList200(Response200):
    # total: int
    # data: List[Message]


# class Response400(Response200):
    # code: int = 400
    # msg: str = "无数据返回"
