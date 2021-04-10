from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from database import Base

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
