from sqlmodel import SQLModel, Field, Column, String, Relationship
from sqlalchemy import ForeignKey, MetaData, JSON
from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import re
from typing import Optional, List
from uuid import uuid4, UUID

from clueless.app.db.models import mapper_registry
from clueless.app.db.models.base import BaseTable
from clueless.app.db.models.user import User


def generate_alphanumeric(length: int = 4) -> str:
    import random, string

    alphanumeric = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    return alphanumeric


class RoomBase(SQLModel):
    name: Optional[str] = Field(index=True)
    player_limit: int = Field(default=6, const=True, index=False)
    is_started: bool = Field(default=False, index=False)
    host: Optional[UUID] = Field(default=None, index=False)


class Room(RoomBase, BaseTable, table=True):
    # WARNING: This does nothing to verify uniqueness other than an error
    room_key: str = Field(unique=True, default_factory=generate_alphanumeric, index=True)

    users: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))


class RoomCreate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: UUID
    room_key: str
    users: List[str]


class RoomUpdate(SQLModel):
    name: Optional[str] = None
    is_started: Optional[bool] = None
    users: Optional[List[str]] = None
