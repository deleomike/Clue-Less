from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.crud.room import RoomCRUD, RoomRead, RoomCreate, RoomUpdate, RoomCreateUI
from clueless.app.db.crud.game import GameCRUD, GameRead, GameCreate
from clueless.app.db import get_session
from clueless.app.core.users import current_active_user
from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session


router = APIRouter()


@router.post("/", response_model=RoomRead)
def create_room(room: RoomCreateUI,
                crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
                user = Depends(current_active_user)):
    room = RoomCreate(name=room.name, host=user.id)
    print("CRUD ROOM: ", room)
    room = crud.create(room=room)
    print("ROOM", room)
    return room


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


@router.post("/{_id}/join/", response_model=RoomRead)
def join_game(_id: str,
               crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
               user = Depends(current_active_user)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    _id = crud.get_by_id_or_key(_id=_id).id

    return crud.add_player(_id=_id, player_id=user.id)


@router.post("/{_id}/start/", response_model=GameRead)
def start_game(_id: str,
               crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
               game_crud: GameCRUD = Depends(GameCRUD.as_dependency),
               user = Depends(current_active_user)):
    """
    Gets the room by either the alphanumeric room key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    room = crud.get_by_id_or_key(_id=_id)

    create = GameCreate(room_id = room.id)

    game = game_crud.create(game=create)

    crud.update(_id=room.id, room=RoomUpdate(is_started=True))

    return game


@router.delete("/{_id}/")
def delete_room(_id: str,
                crud: RoomCRUD = Depends(RoomCRUD.as_dependency),
                user = Depends(current_active_user)):
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






