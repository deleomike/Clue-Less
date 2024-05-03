from fastapi import APIRouter, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from uuid import UUID

from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.character import CharacterCRUD
from clueless import TEMLPATES_PATH, IMAGES_PATH
from clueless.settings import settings

router = APIRouter()

templates = Jinja2Templates(directory=TEMLPATES_PATH)

# Mount the directory where your images are stored
router.mount(IMAGES_PATH, StaticFiles(directory=IMAGES_PATH), name="images")


# class RequiresLogin(Exception):
#   pass
#
#
# @router.exception_handler(RequiresLogin)
# async def requires_login(request: Request, _: Exception):
#     return RedirectResponse(f"/login?next={quote(request.url._url)}")

  

@router.get('/')
def display_index(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@router.get('/register')
def register(request: Request):
  return templates.TemplateResponse("register.html", {"request": request, "settings": settings})


@router.get('/login')
def login(request: Request):
  return templates.TemplateResponse("login.html", {"request": request, "settings": settings})


@router.get("/lobby")
def lobby(request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  rooms = crud.get_all()
  return templates.TemplateResponse("lobby.html", {"request": request, "rooms": rooms, "settings": settings})


@router.get("/delete_room/{room_id}")
def delete_room(request: Request, room_id: str, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  to_del_room = crud.get_by_id_or_key(room_id)
  print("room to delete = ", to_del_room)
  crud.delete(to_del_room.id)
  rooms = crud.get_all()
  return templates.TemplateResponse("lobby.html", {"request": request, "rooms": rooms, "settings": settings})


@router.get('/room/{_id}')
def room(_id: str, request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  room = crud.get_by_id_or_key(_id=_id)
  return templates.TemplateResponse("room.html", {"request": request, "room": room, "settings": settings})


@router.get('/gameboard/{_id}')
def display_gameboard(_id: str, request: Request, crud: RoomCRUD = Depends(RoomCRUD.as_dependency)):
  room = crud.get_by_id_or_key(_id=_id)
  return templates.TemplateResponse("gameboard.html", {"request": request, "room": room, "settings": settings})


@router.get("/game_over/{if_win}")
def lobby(request: Request, if_win: bool):
  return templates.TemplateResponse("game_over.html", {"request": request, "if_win": if_win, "settings": settings})


@router.get("/images/NameBanner")
async def get_banner():
    return FileResponse(str(IMAGES_PATH) + '/NameBanner.png')
  
@router.get("/images/ProfPlum")
async def get_profplum():
    return FileResponse(str(IMAGES_PATH) + '/ProfPlum.png')
  
@router.get("/images/ColMustard")
async def get_colMust():
    return FileResponse(str(IMAGES_PATH) + '/ColMustard.png')
  
@router.get("/images/MrGreen")
async def get_mrgreen():
    return FileResponse(str(IMAGES_PATH) + '/MrGreen.png')
  
@router.get("/images/MrsPeacock")
async def get_mrspeacock():
    return FileResponse(str(IMAGES_PATH) + '/MrsPeacock.png')
  
@router.get("/images/MrsWhite")
async def get_mrswhite():
    return FileResponse(str(IMAGES_PATH) + '/MrsWhite.png')
  
@router.get("/images/MissScar")
async def get_missscar():
    return FileResponse(str(IMAGES_PATH) + '/MissScar.png')
  