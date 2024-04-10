from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.location import Location, LocationRead
from clueless.app.db.models.user import User


class GameBase(SQLModel):
    room_id: UUID = Field(default=None, foreign_key="room.id")

    class Config:
        arbitrary_types_allowed = True


class Game(GameBase, BaseTable, table=True):

    waiting_room: Room = Relationship(
        back_populates="game"
    )

    locations: Optional[list[Location]] = Relationship(
        back_populates="game",
        sa_relationship_kwargs={
            "cascade": "all, delete",  # Instruct the ORM how to track changes to local objects
        },
    )

    characters: Optional[list["Character"]] = Relationship(
        back_populates="game",
        sa_relationship_kwargs={
            "cascade": "all, delete",  # Instruct the ORM how to track changes to local objects
        },
    )

    # TODO: Core game data goes here


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: UUID
    waiting_room: RoomRead | None = None


class GameReadWithLinks(GameRead):
    locations: list[LocationRead]


class GameUpdate(SQLModel):
    pass
