from fastapi import APIRouter

from clueless.app.api import room, session
# from clueless.app.db.models.user import UserCreate, UserRead, UserUpdate
from clueless.app.db.user_schemas import UserCreate, UserRead, UserUpdate
from clueless.app.core.users import auth_backend, current_active_user, fastapi_users

main_router = APIRouter()

main_router.include_router(room.router, prefix="/room", tags=["room", "game"])
main_router.include_router(session.router, prefix="/session", tags=["session"])
main_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
main_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
main_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
main_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


