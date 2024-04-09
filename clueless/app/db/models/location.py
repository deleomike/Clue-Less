from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.room import Room, RoomRead
from clueless.app.db.models.user import User


class LocationLink(SQLModel, table=True):
    origin_id: UUID = Field(default=None, foreign_key="location.id", primary_key=True)
    destination_id: UUID = Field(default=None, foreign_key="location.id", primary_key=True)


class LocationBase(SQLModel):
    game_id: UUID = Field(default=None, foreign_key="game.id")

    name: str = Field(index=True)

    # connections: list[str] = Field(default=None, sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True


class Location(LocationBase, BaseTable, table=True):

    game: "Game" = Relationship(
        back_populates="locations"
    )

    characters: list["Character"] = Relationship(
        back_populates="location"
    )

    connected_locations: list["Location"] = Relationship(
        link_model=LocationLink,
        sa_relationship_kwargs=dict(
            primaryjoin="Location.id==LocationLink.origin_id",
            secondaryjoin="Location.id==LocationLink.destination_id",
        ),
    )

    # TODO: Core game data goes here


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: UUID


class LocationReadLinks(LocationRead):
    connected_locations: list[Location]


class LocationUpdate(SQLModel):
    pass
