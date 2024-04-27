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
from clueless.app.db.crud.card import CardCRUD
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
        self.card_crud = CardCRUD(session=self.session)

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

    @property
    def players(self) -> List[CharacterRead]:
        return [character for character in self.all_characters if character.is_playing]

    @property
    def all_characters(self) -> List[CharacterReadLinks]:
        return self.full_state.characters

    def get_current_turn(self) -> CharacterReadLinks:
        return self.character_crud.get_with_link(self.full_state.character_turn_id)

    def is_my_turn(self, user_id: UUID) -> bool:
        character = self.get_character_info(user_id=user_id)

        return character.id == self.get_current_turn().id

    def is_character_turn(self, character_id: UUID) -> bool:

        return character_id == self.get_current_turn().id

    def get_character_by_name(self, character_name) -> CharacterRead:
        characters = self.all_characters

        for character in characters:
            if character.name == character_name:
                return character

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

        locations = []
        for location in location.connected_locations:
            if "-" in location.name:
                if len(location.characters) == 0:
                    locations.append(location)
            else:
                locations.append(location)

        return locations

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

        if self.full_state.game_over:
            raise HTTPException(status_code=500, detail="Game is over")

        if validate:
            valid = self.is_valid_location_move(character_id=character_id, location_id=location_id)

            if not valid:
                raise Exception("Invalid move for character.")

            if not self.is_character_turn(character_id):
                raise HTTPException(status_code=500, detail="Not the character's turn")

        self.character_crud.change_room(id=character_id, location_id=location_id)

        if validate:
            character = self.character_crud.get_with_link(character_id)

            if "-" in character.location:
                # hallway end turn
                self.game_crud.increment_turn(self.id)

        return self.character_crud.get_with_link(character_id)


    def make_suggestions(self, current_character_id: UUID, character_name: str, weapon_name: str) -> CardRead:
        """
        Go round the table and make suggestions
        :param current_player:
        :param character_name:
        :param weapon_name:
        :return:
        """
        if not self.is_character_turn(current_character_id):
            raise HTTPException(status_code=500, detail="Not the character's turn")

        if self.full_state.game_over:
            raise HTTPException(status_code=500, detail="Game is over")

        current_player = self.character_crud.get_with_link(current_character_id)

        chosen_character = self.get_character_by_name(character_name=character_name)

        if "-" in current_player.location.name:
            raise HTTPException(status_code=500, detail="Cannot make a suggestion from a hallway")

        # teleport the character
        self.move_player(character_id=chosen_character.id, location_id=current_player.location_id, validate=False)

        for player in self.players:
            if player.id == current_character_id:
                continue
            else:
                card = self.make_suggestion(
                    current_player=current_character_id,
                    accused_id=player.id,
                    character_name=character_name,
                    weapon_name=weapon_name
                )
                if card is not None:
                    return card

        self.game_crud.increment_turn(self.id)


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

        if "-" in current_player.location.name:
            raise Exception("Cannot make a suggestion from a hallway")

        # # teleport the accused
        # self.move_player(character_id=accused_id, location_id=current_player.location_id, validate=False)

        # TODO Card checking for this player and maybe others

        matching_cards = []
        for name in [weapon_name, character_name, current_player.location.name]:
            for card in self.character_crud.get_owned_cards(character_id=accused_id):
                if name == card.name:
                    matching_cards.append(card)

        if len(matching_cards) == 0:
            return None

        #return one matching card
        card = random.choice(matching_cards)
        self.card_crud.link_to_character(card.id, current_player)

        return card

    def _set_player_lost(self, character_id: UUID):
        character = CharacterUpdate(is_playing=False, is_won=False)

        self.character_crud.update(_id=character_id, character=character)

        if len(self.players) == 1:
            #last player
            self._set_player_won(self.players[0].id)

    def _set_player_won(self, character_id: UUID):
        character = CharacterUpdate(is_won=True)

        self.character_crud.update(_id=character_id, character=character)

        self.game_crud.set_win(self.id, game_over=True)

    def make_accusation(self, current_player_id: UUID, player_name: str, room_name: str, weapon: str) -> bool:
        """
        Make an accusation, checks the game's cards.

        TODO: Make the player lose, add a field for lost or not to the character db
        TODO: Return all cards?

        UNTESTED

        :param current_player_id:
        :param player_name:
        :param room_name:
        :param weapon:
        :return:
        """
        if self.full_state.game_over:
            raise HTTPException(status_code=500, detail="Game is over")

        won = self.is_solution(character=player_name, weapon=weapon, location=room_name)

        if won:
            # TODO: set game to winning
            self._set_player_won(character_id=current_player_id)
        else:
            self.game_crud.increment_turn(self.id)
            # TODO set player to having lost
            self._set_player_lost(character_id=current_player_id)

        return won
