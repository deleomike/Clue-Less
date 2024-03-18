from sqlmodel import select
from typing import List
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.room import RoomBase, Room, RoomRead, RoomCreate


class RoomCRUD(BaseCRUD):

    def get(self, _id: UUID) -> RoomRead:
        room = self.session.get(Room, _id)
        if not room:
            raise HTTPException(status_code=404, detail="Hero not found")
        return room

    def get_all(self) -> List[RoomRead]:
        rooms = self.session.exec(select(Room)).all()
        return rooms

    def create(self, room: RoomCreate) -> RoomRead:
        db_room = Room.model_validate(room)
        self.session.add(db_room)
        self.session.commit()
        self.session.refresh(db_room)
        return db_room

