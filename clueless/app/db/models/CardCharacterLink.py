from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID


class CardCharacterLink(SQLModel, table=True):
    character_id: UUID | None = Field(default=None, foreign_key="character.id", primary_key=True)
    card_id: UUID | None = Field(default=None, foreign_key="card.id", primary_key=True)
