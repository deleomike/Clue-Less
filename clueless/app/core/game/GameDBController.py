import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.game import GameCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationRead
from clueless.app.db.crud.character import CharacterCRUD, CharacterRead
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate, GameReadWithLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate, CharacterUpdate



class GameDBController:

    def __init__(self, id: UUID, session):
        self.id = id

        self.session = session
        self.game_crud = GameCRUD(session=self.session)
        self.location_crud = LocationCRUD(session=self.session)
        self.character_crud = CharacterCRUD(session=self.session)

    @property
    def full_state(self) -> GameRead:
        return self.game_crud.get(self.id)

    def valid_moves(self):
        pass

    def get_adjacent_locations(self, location_id: UUID) -> List[LocationRead]:
        location = self.location_crud.get(location_id)

        return location.connected_locations

    def is_valid_location_move(self, character_id: UUID, location_id: UUID):
        pass

    def get_character_info(self, user_id: UUID) -> CharacterRead:
        return self.character_crud.get_by_user_id(user_id=str(user_id))

    def move_player(self, character_id: UUID, location_id: UUID, validate: bool = False):
        ccrud = CharacterCRUD(session=self.session)

        character = ccrud.get(character_id)

        CharacterUpdate()