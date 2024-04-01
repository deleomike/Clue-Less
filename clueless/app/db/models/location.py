from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.user import User


class LocationBase(SQLModel):
    game_id: UUID = Field(default=None, foreign_key="game.id")

    name: str = Field(index=True)

    class Config:
        arbitrary_types_allowed = True


class Location(LocationBase, BaseTable, table=True):

    game: "Game" = Relationship(
        back_populates="locations"
    )

    characters: list["Game"] = Relationship(
        back_populates="location"
    )

    # TODO: Core game data goes here


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: UUID


class LocationUpdate(SQLModel):
    pass
