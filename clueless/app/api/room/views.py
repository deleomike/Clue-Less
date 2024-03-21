from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.crud.room import RoomCRUD, RoomRead, RoomCreate, RoomUpdate
from clueless.app.db import get_session
from clueless.app.core.users import fastapi_users
from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session


router = APIRouter()


@router.post("/", response_model=RoomRead)
def create_room(room: RoomCreate,
                crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
                current_active_user = fastapi_users.current_user(active=True)):
    return crud.create(room=room)


@router.get("/", response_model=List[RoomRead])
def get_all(crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
    return crud.get_all()


@router.get("/{_id}/", response_model=RoomRead)
def get_room_info(_id: str,
                  crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    return crud.get_by_id_or_key(_id=_id)


@router.post("/{_id}/join/", dependencies=[Depends(session.cookie)])
def join_game(_id: str,
               crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
               current_active_user = fastapi_users.current_user(active=True)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    _id = crud.get_by_id_or_key(_id=_id).id

    return crud.update(_id=_id, room=RoomUpdate(is_started=True))


@router.post("/{_id}/start/", dependencies=[Depends(session.cookie)], response_model=RoomRead)
def start_game(_id: str,
               crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
               current_active_user = fastapi_users.current_user(active=True)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    room = crud.get_by_id_or_key(_id=_id)

    return crud.update(_id=room.id, room=RoomUpdate(is_started=True))


@router.delete("/{_id}/", response_model=RoomRead)
def delete_room(_id: str,
                crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
                current_active_user = fastapi_users.current_user(active=True)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    room = crud.get_by_id_or_key(_id=_id)

    return {
        "status": crud.delete(room.id)
    }






