from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.user import User


class CardBase(SQLModel):
    game_id: Optional[UUID] = Field(default=None, foreign_key="game.id")
    character_id: Optional[UUID] = Field(default=None, foreign_key="character.id")

    name: str = Field(index=True)
    type: str = Field(index=True)


class Card(CardBase, BaseTable, table=True):

    game: Optional["Game"] = Relationship(
        back_populates="solution"
    )

    character: Optional["Character"] = Relationship(
        back_populates="hand"
    )

    # TODO: Core game data goes here


class CardCreate(CardBase):
    pass


class CardRead(CardBase):
    id: UUID


class CardUpdate(SQLModel):
    pass
