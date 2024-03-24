import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.room import RoomBase, Room, RoomRead, RoomCreate, RoomUpdate, RoomCreateUI


class RoomCRUD(BaseCRUD):

    def get_by_id_or_key(self, _id: Union[str, UUID]) -> RoomRead:
        """
        Gets the room by either the alphanumeric room key or by the ID
        :param _id:
        :return:
        """
        # try string to UUID conversion
        if isinstance(_id, str):
            try:
                uuid_obj = UUID(_id)
                _id = uuid_obj
            except ValueError:
                pass

        # Get room by uuid
        if isinstance(_id, UUID):
            return self.get(_id=_id)
        # Get room by room_key
        elif isinstance(_id, str):
            return self.get_by_room_key(room_key=_id)
        # Invalid ID
        else:
            raise HTTPException(status_code=500, detail=f"Invalid type for id, {type(_id)}")

    def get_by_room_key(self, room_key: str) -> RoomRead:
        return self.session.exec(select(Room).where(Room.room_key == room_key)).one()

    def get(self, _id: UUID) -> RoomRead:
        room = self.session.get(Room, _id)
        if not room:
            raise HTTPException(status_code=404, detail="Hero not found")
        return room

    def get_all(self) -> List[RoomRead]:
        rooms = self.session.exec(select(Room)).all()
        return rooms

    def create(self, room: RoomCreate) -> RoomRead:
        print("CREATE")
        # room.users = [str(room.host)]
        db_room = Room.model_validate(room)
        db_room.users = [str(room.host)]
        self.session.add(db_room)
        self.session.commit()
        self.session.refresh(db_room)

        return db_room

    def delete(self, _id: UUID) -> RoomRead:
        room = self.session.get(Room, _id)
        if not room:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.session.delete(room)
        self.session.commit()
        return True

    def update(self, _id: UUID, room: RoomUpdate) -> RoomRead:
        db_room = self.session.get(Room, _id)
        if not db_room:
            raise HTTPException(status_code=404, detail="Room not found")
        room_data = room.model_dump(exclude_unset=True)
        db_room.sqlmodel_update(room_data)
        self.session.add(db_room)
        self.session.commit()
        self.session.refresh(db_room)
        return db_room


    def add_player(self, _id: UUID, player_id: UUID) -> RoomRead:
        room = self.get(_id=_id)

        new_room = RoomUpdate(users=room.users)
        new_room.users.append(str(player_id))

        return self.update(_id=_id, room=new_room)
