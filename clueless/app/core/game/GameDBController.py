import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationCreate
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate, GameReadWithLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate, CharacterUpdate



class GameDBController:

    def __init__(self):
        pass

    def move_player(self, id: UUID, character_id: UUID, location_id: UUID, validate: bool = False):
        ccrud = CharacterCRUD(session=self.session)

        character = ccrud.get(character_id)

        CharacterUpdate()