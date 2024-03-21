from uuid import uuid4, UUID
from pydantic import BaseModel
from typing import Dict


class SessionCreate(BaseModel):
    username: str


class SessionData(SessionCreate):
    id: UUID = uuid4()

