from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.crud.room import RoomCRUD, RoomRead, RoomCreate
from clueless.app.db import get_session

router = APIRouter()


@router.post("/", response_model=RoomRead)
def create_room(room: RoomCreate, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
    return crud.create(room=room)


@router.get("/", response_model=List[RoomRead])
def get_all(crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
    return crud.get_all()


@router.get("/{_id}", response_model=RoomRead)
def get_room_info(_id: UUID, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
    return crud.get(_id=_id)






