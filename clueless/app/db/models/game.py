from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models import mapper_registry
from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.user import User


class GameBase(SQLModel):
    room_id: UUID = Field(default=None, foreign_key="room.id")

    class Config:
        arbitrary_types_allowed = True


class Game(GameBase, BaseTable, table=True):

    room: Room = Relationship(
        back_populates="game"
    )


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: UUID
    room: RoomRead | None = None


class GameUpdate(SQLModel):
    pass
