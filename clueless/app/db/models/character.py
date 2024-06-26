from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.CardCharacterLink import CardCharacterLink
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.user import User


class CharacterBase(SQLModel):
    game_id: UUID = Field(default=None, foreign_key="game.id")
    location_id: UUID = Field(default=None, foreign_key="location.id")
    user_id: Optional[str] = Field(index=True)

    name: str = Field(index=True)

    is_playing: bool = Field(default=True, index=False)
    is_won: bool = Field(default=False, index=False)
    # is_turn: bool = Field(default=False, index=False)

    class Config:
        arbitrary_types_allowed = True


class Character(CharacterBase, BaseTable, table=True):

    game: "Game" = Relationship(
        back_populates="characters"
    )

    location: "Location" = Relationship(
        back_populates="characters"
    )

    hand: Optional[list["Card"]] = Relationship(
        back_populates="characters",
        link_model=CardCharacterLink
    )

    # TODO: Core game data goes here


class CharacterCreate(CharacterBase):
    pass


class CharacterRead(CharacterBase):
    id: UUID


class CharacterUpdate(SQLModel):
    is_playing: Optional[bool] = None
    is_won: Optional[bool] = None
    # is_turn: Optional[bool] = None
