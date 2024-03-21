import re

from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey, MetaData


class BaseTable(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    class Config:
        arbitrary_types_allowed = True
