import uuid
import random

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.game import GameCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationRead
from clueless.app.db.models.shared import CharacterReadLinks, LocationReadLinks, GameReadWithLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterRead
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate, CharacterUpdate
from clueless.app.db.models.card import CardRead



class GameDBController:
    """
    The main interface for
    """

    def __init__(self, game_id: UUID, session):
        self.id = game_id

        self.session = session
        self.game_crud = GameCRUD(session=self.session)
        self.location_crud = LocationCRUD(session=self.session)
        self.character_crud = CharacterCRUD(session=self.session)

    @property
    def full_state(self) -> GameReadWithLinks:
        """
        Full Game State

        :return:
        """
        return self.game_crud.get(self.id)

    def get_adjacent_character_locations(self, character_id: UUID) -> List[LocationRead]:
        """
        Get the rooms adjacent to the character

        :param character_id:
        :return:
        """
        character = self.character_crud.get_with_link(character_id)

        return self.get_adjacent_locations(location_id=character.location_id)


    def get_adjacent_locations(self, location_id: UUID) -> List[LocationRead]:
        """
        Get the adjacent rooms to a given location.

        :param location_id:
        :return:
        """
        location = self.location_crud.get(location_id)

        return location.connected_locations

    def is_valid_location_move(self, character_id: UUID, location_id: UUID) -> bool:
        """
        Checks whether a move is invalid (no connection between locations)

        :param character_id:
        :param location_id:
        :return:
        """
        character = self.character_crud.get_with_link(character_id)

        if character.location_id == location_id:
            # Can't move to their own room
            return False

        for location in self.get_adjacent_locations(location_id=character.location_id):
            if location.id == location_id:
                return True

        return False

    def get_character_info(self, user_id: UUID) -> CharacterReadLinks:
        """
        Gets the character info by the user's ID

        :param user_id:
        :return:
        """
        return self.character_crud.get_by_user_id(user_id=str(user_id))

    def move_player_location_name(self, character_id: UUID, location_name: str, validate: bool = False) -> CharacterReadLinks:
        """
        Move a character to a new room by the name of the room

        :param character_id:
        :param location_name:
        :param validate:
        :return:
        """
        game = self.full_state

        for location in game.locations:
            if location.name == location_name:
                return self.move_player(
                    character_id=character_id,
                    location_id=location.id,
                    validate=validate
                )

    def move_player(self, character_id: UUID, location_id: UUID, validate: bool = False) -> CharacterReadLinks:
        """
        Move a character to a new room by the location's id

        :param character_id:
        :param location_id:
        :param validate:
        :return:
        """
        if validate:
            valid = self.is_valid_location_move(character_id=character_id, location_id=location_id)

            if not valid:
                raise Exception("Invalid move for character.")

        self.character_crud.change_room(id=character_id, location_id=location_id)

        return self.character_crud.get_with_link(character_id)

    def make_suggestion(self, current_player: UUID, accused_id: UUID, weapon: str) -> CardRead:
        current_player = self.character_crud.get_with_link(current_player)
        accused_player = self.character_crud.get_with_link(accused_id)

        if "hallway" in current_player.location.name:
            raise Exception("Cannot make a suggestion from a hallway")

        # teleport the accused
        self.move_player(character_id=accused_id, location_id=current_player.location_id, validate=False)

        # TODO Card checking for this player and maybe others

        matching_cards = []
        for name in [weapon, accused_player.name, current_player.location.name]:
            for card in accused_player.hand:
                if name == card.name:
                    matching_cards.append(card)

        #return one matching card
        return random.choice(matching_cards)
