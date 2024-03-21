from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from clueless.app.db.crud.user import UserCRUD, UserRead, UserCreate, UserUpdate
from clueless.app.db import get_session
from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session

router = APIRouter()


@router.post("/")
def create_user(user: UserCreate,
                crud: UserCRUD = Depends(UserCRUD.as_dependency)):
    return crud.create(user=user)


@router.get("/", response_model=List[UserRead])
def get_all(crud: UserCRUD = Depends(UserCRUD.as_dependency)):
    return crud.get_all()


@router.get("/{_id}/", response_model=UserRead)
def get_user_info(_id: str, crud: UserCRUD = Depends(UserCRUD.as_dependency)):
    """
    Gets the user by either the alphanumeric user key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    return crud.get_by_id_or_key(_id=_id)


@router.post("/{_id}/join/", dependencies=[Depends(session.cookie)])
def start_game(_id: str,
               crud: UserCRUD = Depends(UserCRUD.as_dependency),
               session_data: SessionData = Depends(session.verifier)):
    """
    Gets the user by either the alphanumeric user key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    _id = crud.get_by_id_or_key(_id=_id).id

    return crud.update(_id=_id, user=UserUpdate(is_started=True))


@router.post("/{_id}/start/", dependencies=[Depends(session.cookie)], response_model=UserRead)
def start_game(_id: str, crud: UserCRUD = Depends(UserCRUD.as_dependency)):
    """
    Gets the user by either the alphanumeric user key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    user = crud.get_by_id_or_key(_id=_id)

    return crud.update(_id=user.id, user=UserUpdate(is_started=True))


@router.delete("/{_id}/", response_model=UserRead)
def delete_user(_id: str, crud: UserCRUD = Depends(UserCRUD.as_dependency)):
    """
    Gets the user by either the alphanumeric user key or by the ID
    :param _id:
    :param crud:
    :return:
    """
    user = crud.get_by_id_or_key(_id=_id)

    return {
        "status": crud.delete(user.id)
    }






