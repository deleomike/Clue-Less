from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4


class RoomBase(SQLModel):
    name: Optional[str] = Field(index=True)


class Room(RoomBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class RoomCreate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: UUID
