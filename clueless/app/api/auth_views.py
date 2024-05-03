from fastapi import APIRouter, Depends

from clueless.app.db.user_schemas import UserRead
from clueless.app.core.users import current_active_user

router = APIRouter()

@router.get("/whoami", response_model=UserRead)
def whoami(user = Depends(current_active_user)):
    return user