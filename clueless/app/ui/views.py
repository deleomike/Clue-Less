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


@router.get('/register')
def login_page(request: Request):
  return templates.TemplateResponse("register.html", {"request": request})


@router.get('/login')
async def login(request: Request):
  return templates.TemplateResponse("login.html", {"request": request})

@router.get("/waiting_room/{name}")
def get_waiting_room(request: Request, name: str):
  if name is None:
    return "name not found in URL"
  print(name)
  return templates.TemplateResponses("waiting_room.html", {"request": request, "curr_player":name})


@router.get('/rooms')
def rooms(request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  rooms = crud.get_all()
  return templates.TemplateResponse("rooms.html", {"request": request, "rooms":rooms})


@router.get('/rooms/{_id}')
def room(_id: str, request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  room = crud.get_by_id_or_key(_id=_id)
  return templates.TemplateResponse("room.html", {"request": request, "room": room})
