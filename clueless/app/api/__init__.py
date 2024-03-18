from fastapi import APIRouter

from clueless.app.api import room, session

main_router = APIRouter()

main_router.include_router(room.router, prefix="/room", tags=["room", "game"])
main_router.include_router(session.router, prefix="/session", tags=["session"])


