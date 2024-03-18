from typing import Union, Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import (
    Cookie,
    Request,
    WebSocketDisconnect,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)


from clueless.app.core.ConnectionManager import ConnectionManager
from clueless import STATIC_PATH, TEMLPATES_PATH
from clueless.app.api import main_router

app = FastAPI()
manager = ConnectionManager()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMLPATES_PATH)

app.include_router(main_router)


# @app.get('/')
# def home(request: Request):
#   return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
def on_startup():
    from clueless.app.db import create_db_and_tables
    create_db_and_tables()

@app.get('/')
def home(request: Request):
  return templates.TemplateResponse("chat2.html", {"request": request})


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")