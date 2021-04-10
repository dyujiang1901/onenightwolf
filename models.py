from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from database import Base

# class Message(Base):
    # __tablename__ = "message"
    # id = Column(Integer, primary_key=True, index=True)
    # name = Column(String(60), comment="昵称", nullable=False)
    # body = Column(String(200), comment="内容", nullable=False)
    # create_at = Column(DateTime, default=datetime.now, comment="创建时间")


class Game(Base):
    __tablename__ = "game"

    rmid = Column(Integer, comment="room number", primary_key= True, nullable=False)
    rolesinit = Column(String(200), comment="init roles", nullable=False)
    rolesingame = Column(String(200), default=rolesinit)

class Player(Base):
    __tablename__ = "player"

    rmid = Column(Integer, comment="room number", nullable=False)
    pos = Column(Integer, comment="position", nullable=False)
    name = Column(String(200), comment="name", nullable=False)
    op1 = Column(Integer)
    op2 = Column(Integer)
    awaken = Column(Integer)
    voted = Column(Integer)
    id = Column(Integer, comment="DB id", primary_key=True)
