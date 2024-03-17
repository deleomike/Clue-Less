from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Response, Depends
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session


router = APIRouter()




# @router.post("/")
# async def create_session(payload: SessionCreate, response: Response):
#     data = SessionData(username=payload.username)
#
#     await backend.create(data.id, data)
#     cookie.attach_to_response(response, data.id)
#
#     return f"created session for {data.username}"
#
#
# @router.get("/", dependencies=[Depends(cookie)])
# async def whoami(session_data: SessionData = Depends(verifier)):
#     return session_data
#
#
# @router.delete("/")
# async def del_session(response: Response, session_id: UUID = Depends(cookie)):
#     await backend.delete(session_id)
#     cookie.delete_from_response(response)
#     return "deleted session"


@router.post("/")
async def create_session(payload: SessionCreate, response: Response):

    return await session.create(data=payload, response=response)


@router.get("/", dependencies=[Depends(session.cookie)])
async def whoami(session_data: SessionData = Depends(session.verifier)):
    return session_data


@router.delete("/")
async def del_session(response: Response, session_id: UUID = Depends(session.cookie)):
    if await session.delete(response=response, session_id=session_id):
        return "deleted session"
    else:
        return "Something went wrong"
