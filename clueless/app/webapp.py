from typing import Union, Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
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
from clueless.app.ui.views import router as ui_router
from clueless.app.core.users import current_active_user
from clueless.app.db.models.user import User


app = FastAPI()
manager = ConnectionManager()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
templates = Jinja2Templates(directory=TEMLPATES_PATH)

app.include_router(main_router, prefix="/api")
app.include_router(ui_router)

origins = ["http://localhost:8080", "https://localhost", "http://127.0.0.1:8080", "http://127.0.0.1"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get('/')
# def home(request: Request):
#   return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def on_startup():
    from clueless.app.db import create_db_and_tables, alchemy_create_db_and_tables
    create_db_and_tables()
    await alchemy_create_db_and_tables()



async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token



@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="webapp:app", reload=True, host="127.0.0.1", port=8000)
