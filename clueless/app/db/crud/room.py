import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.models.room import RoomBase, Room, RoomRead, RoomCreate, RoomUpdate


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
        self.session.add(db_room)
        self.session.commit()
        self.session.refresh(db_room)

        return self.add_player(_id=db_room.id, player_id=room.host)

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
        print("ADDPlayer")
        player_string = str(player_id.__str__())
        print("PLAYER ID ", player_string)
        print(type(player_string))
        print(type(player_id))
        room = self.get(_id=_id)

        if room.users is None:
            room.users = []

        # if player_id in room.users:
        #     raise HTTPException(500, detail="User already added")
        room.users.append(str(player_string))
        print(room.users)

        # update = RoomUpdate.model_validate(room)

        # print("UPDATE ", update)

        # return self.update(_id=_id, room=update)
        #
        # print(room)

        self.session.add(room)
        self.session.commit()

        room = self.get(_id=_id)

        print(room)

        return self.get(_id)