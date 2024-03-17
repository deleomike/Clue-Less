from fastapi import APIRouter

from clueless.app.api.room import router

main_router = APIRouter()

main_router.include_router(router, prefix="room")


