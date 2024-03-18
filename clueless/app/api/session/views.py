from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Response, Depends
from uuid import UUID, uuid4

from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session


router = APIRouter()


@router.post("/")
async def create_session(payload: SessionCreate, response: Response):
    """
    Creates the user session

    :param payload:
    :param response:
    :return:
    """

    return await session.create(data=payload, response=response)


@router.get("/", dependencies=[Depends(session.cookie)])
async def whoami(session_data: SessionData = Depends(session.verifier)):
    """
    Returns session data for current user

    :param session_data:
    :return:
    """
    return session_data


@router.delete("/")
async def del_session(response: Response, session_id: UUID = Depends(session.cookie)):
    """
    Deletes the user session

    :param response:
    :param session_id:
    :return:
    """
    if await session.delete(response=response, session_id=session_id):
        return "deleted session"
    else:
        return "Something went wrong"
