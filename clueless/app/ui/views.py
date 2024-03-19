from fastapi import APIRouter, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import UUID

from clueless.app.db.crud.room import RoomCRUD
from clueless.app.core.session import SessionData, SessionCreate, SessionCRUD, BasicVerifier, session
from clueless import TEMLPATES_PATH

router = APIRouter()

templates = Jinja2Templates(directory=TEMLPATES_PATH)


# class RequiresLogin(Exception):
#   pass
#
#
# @router.exception_handler(RequiresLogin)
# async def requires_login(request: Request, _: Exception):
#     return RedirectResponse(f"/login?next={quote(request.url._url)}")


@router.get('/')
def index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@router.get('/login', dependencies=[Depends(session.cookie)])
async def login(request: Request, session_data: SessionData = Depends(session.verifier)):
  print("HELLO")
  data = await session.whoami(reqeust=request)
  print(data)
  return templates.TemplateResponse("login.html", {"request": request})


@router.get('/rooms')
def rooms(request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  rooms = crud.get_all()
  return templates.TemplateResponse("rooms.html", {"request": request, "rooms":rooms})


@router.get('/rooms/{_id}')
def room(_id: str, request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  room = crud.get_by_id_or_key(_id=_id)
  return templates.TemplateResponse("room.html", {"request": request, "room": room})
