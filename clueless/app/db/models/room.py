from sqlmodel import SQLModel, Field, Column, String
from typing import Optional
from uuid import UUID, uuid4


def generate_alphanumeric(length: int = 4) -> str:
    import random, string

    alphanumeric = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    return alphanumeric


class RoomBase(SQLModel):
    name: Optional[str] = Field(index=True)
    player_limit: int = Field(default=6, const=True, index=False)
    is_started: bool = Field(default=False, index=False)


class Room(RoomBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # WARNING: This does nothing to verify uniqueness other than an error
    room_key: str = Field(unique=True, default_factory=generate_alphanumeric, index=True)


class RoomCreate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: UUID
    room_key: str


class RoomUpdate(SQLModel):
    name: Optional[str] = None
    is_started: Optional[bool] = None
