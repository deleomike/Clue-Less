from pydantic import BaseModel

from clueless.app.db.models.card import CardRead


class SuggestionRequest(BaseModel):

    weapon_name: str
    character_name: str

class suggestion_response(BaseModel):

    revealed_card: CardRead = None
    message: str


class AccusationRequest(SuggestionRequest):
    room_name: str
