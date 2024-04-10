import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.game import GameCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationRead
from clueless.app.db.models.shared import CharacterReadLinks, LocationReadLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterRead
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate, GameReadWithLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate, CharacterUpdate



class GameDBController:

    def __init__(self, game_id: UUID, session):
        self.id = game_id

        self.session = session
        self.game_crud = GameCRUD(session=self.session)
        self.location_crud = LocationCRUD(session=self.session)
        self.character_crud = CharacterCRUD(session=self.session)

    @property
    def full_state(self) -> GameRead:
        return self.game_crud.get(self.id)

    def get_adjacent_character_locations(self, character_id: UUID) -> List[LocationRead]:
        character = self.character_crud.get_with_link(character_id)

        return self.get_adjacent_locations(location_id=character.location_id)


    def get_adjacent_locations(self, location_id: UUID) -> List[LocationRead]:
        location = self.location_crud.get(location_id)

        return location.connected_locations

    def is_valid_location_move(self, character_id: UUID, location_id: UUID) -> bool:
        character = self.character_crud.get_with_link(character_id)

        if character.location_id == location_id:
            # Can't move to their own room
            return False

        for location in self.get_adjacent_locations(location_id=character.location_id):
            if location.id == location_id:
                return True

        return False

    def get_character_info(self, user_id: UUID) -> CharacterReadLinks:
        return self.character_crud.get_by_user_id(user_id=str(user_id))

    def move_player(self, character_id: UUID, location_id: UUID, validate: bool = False) -> CharacterReadLinks:
        if validate:
            valid = self.is_valid_location_move(character_id=character_id, location_id=location_id)

            if not valid:
                raise Exception("Invalid move for character.")

        self.character_crud.change_room(id=character_id, location_id=location_id)

        return self.character_crud.get_with_link(character_id)