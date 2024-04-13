import uuid
import random

from sqlmodel import select
from typing import List, Union, Tuple
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


    @property
    def solution(self) -> Tuple[CardRead, CardRead, CardRead]:
        """
        Solution

        :return:
        """
        sol = self.full_state.solution

        return (sol[0], sol[1], sol[2])

    @property
    def weapon_card_list(self) -> List[str]:
        return self.game_crud.WEAPON_NAMES

    @property
    def location_card_list(self) -> List[str]:
        return self.game_crud.LOCATION_NAMES

    @property
    def character_card_list(self) -> List[str]:
        return self.game_crud.DEFAULT_NAMES

    def is_solution(self, character: str, weapon: str, location: str):
        solution = self.solution

        return {character, weapon, location} == set(card.name for card in solution)

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

        UNTESTED

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

    def print_character_info(self, character_id: UUID):

        character = self.character_crud.get_with_link(character_id)

        print(f"Name: {character.name}")
        print(f"Location: {character.location.name}")
        print(f"Adjacent Locations: {[location.name for location in self.get_adjacent_character_locations(character_id=character_id)]}")
        print(f"Cards: {[card.name for card in character.hand]}")

    def get_character_info(self, user_id: UUID) -> CharacterReadLinks:
        """
        Gets the character info by the user's ID

        UNTESTED

        :param user_id:
        :return:
        """
        return self.character_crud.get_by_user_id(user_id=str(user_id))

    def move_player_location_name(self, character_id: UUID, location_name: str, validate: bool = False) -> CharacterReadLinks:
        """
        Move a character to a new room by the name of the room

        UNTESTED

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

        UNTESTED

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

    def make_suggestion(self, current_player: UUID, accused_id: UUID, character_name: str, weapon_name: str) -> CardRead:
        """
        Makes a suggestion.

        teleports the accused and checks their cards.

        TODO: Probably not checking their cards specifically
        TODO: Implement character name logic instead here

        UNTESTED

        :param current_player:
        :param accused_id:
        :param weapon:
        :return:
        """
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

    def make_accusation(self, current_player: UUID, player_name: str, room_name: str, weapon: str) -> bool:
        """
        Make an accusation, checks the game's cards.

        TODO: Make the player lose, add a field for lost or not to the character db
        TODO: Return all cards?

        UNTESTED

        :param current_player:
        :param player_name:
        :param room_name:
        :param weapon:
        :return:
        """
        current_player = self.character_crud.get_with_link(current_player)

        if "hallway" in current_player.location.name:
            raise Exception("Cannot make a suggestion from a hallway")

        game = self.full_state

        names = set([card.name for card in game.solution])

        match = ({player_name, room_name, weapon} == names)

        return match
