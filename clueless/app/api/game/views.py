from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.models.game import GameRead, GameCreate, GameUpdate
from clueless.app.db.crud.game import GameCRUD
from clueless.app.db import get_session
from clueless.app.core.users import current_active_user
from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session


router = APIRouter()


@router.get("/", response_model=List[GameRead])
def get_all(crud: GameCRUD = Depends(GameCRUD.as_dependency)):
    return crud.get_all()


@router.get("/{_id}/", response_model=GameRead)
def get_game_info(_id: str,
                  crud: GameCRUD = Depends(GameCRUD.as_dependency)):
    """
    Gets the game by either the alphanumeric game key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    return crud.get_by_id_or_key(_id=_id)


@router.delete("/{_id}/")
def delete_game(_id: str,
                crud: GameCRUD = Depends(GameCRUD.as_dependency),
                user = Depends(current_active_user)):
    """
    Gets the game by either the alphanumeric game key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    game = crud.get_by_id_or_key(_id=_id)

    return {
        "status": crud.delete(game.id)
    }






