import math
import uuid

from copy import deepcopy
from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationCreate
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate, CharacterRead, CharacterUpdate
from clueless.app.db.crud.card import CardCRUD, CardCreate
from clueless.app.db.models.shared import GameReadWithLinks


class GameCRUD(BaseCRUD):
    DEFAULT_NAMES = ["Prof. Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White", "Col. Mustard", "Miss Scarlet"]
    LOCATION_NAMES = [
        "Study",
        "Hall",
        "Lounge",
        "Dining Room",
        "Billiard Room",
        "Library",
        "Conservatory",
        "Ball Room",
        "Kitchen"
    ]
    WEAPON_NAMES = [
        "Candlestick",
        "Dagger",
        "Lead Pipe",
        "Revolver",
        "Rope",
        "Wrench"
    ]

    STARTING_LOCATIONS = [
                          "Study-Library Hall",
                          "Library-Conservatory Hall",
                          "Conservatory-Ball Room Hall",
                          "Ball Room-Kitchen Hall",
                          "Hall-Lounge Hall",
                          "Lounge-Dining Room Hall",
                          ]

    def get(self, _id: UUID) -> GameReadWithLinks:
        game = self.session.get(Game, _id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    def get_all(self) -> List[GameRead]:
        games = self.session.exec(select(Game)).all()
        return games

    def populate_characters(self, id: UUID, character_names: List[str] = None) -> GameReadWithLinks:
        # for now, place all in the first room
        game = self.get(id)
        ccrud = CharacterCRUD(session=self.session)

        if character_names is None:
            character_names = self.DEFAULT_NAMES

        user_ids = ["" for _ in character_names]
        for i, user_id in enumerate(game.waiting_room.users):
            user_ids[i] = user_id

        assert (len(user_ids) == len(character_names))

        print("USER IDS: ", user_ids)
        starting_locations = {location.name : location.id for location in game.locations if "-" in location.name}
        for user, name, hallway_name in zip(user_ids, character_names, self.STARTING_LOCATIONS):
            create = CharacterCreate(
                name=name,
                user_id=user,
                location_id=starting_locations[hallway_name],
                game_id=game.id,
                is_playing=(user != "")  # False if user is ""
            )

            ccrud.create(character=create)

        return self.get(id)

    def _deal_cards(self, game_id: UUID):
        locations, weapons, characters = deepcopy(self.LOCATION_NAMES), deepcopy(self.WEAPON_NAMES), deepcopy(
            self.DEFAULT_NAMES)
        card_details = []
        import random

        random.shuffle(locations)
        random.shuffle(weapons)
        random.shuffle(characters)

        solution = ((locations.pop(), "room"), (weapons.pop(), "weapon"), (characters.pop(), "character"))

        card_details.extend([(name, "character") for name in characters])
        card_details.extend([(name, "room") for name in locations])
        card_details.extend([(name, "weapon") for name in weapons])

        ########
        # Adjust how many characters get how many cards
        game: GameReadWithLinks = self.get(game_id)
        card_character_multiple = math.ceil(len(card_details) / len(game.characters))
        characters_ = (game.characters * card_character_multiple)[:len(card_details)]
        random.shuffle(characters_)
        ########

        cards = [CardCreate(name=details[0], type=details[1], owner_id=character.id, owner_name=character.name)
                 for details, character in zip(card_details, characters_)]

        solution_cards = [CardCreate(name=name, type=type, game_id=game_id) for name, type in solution]

        cards.extend(solution_cards)

        card_crud = CardCRUD(session=self.session)

        for card in cards:
            card_crud.create(card)

    def create(self, game: GameCreate, character_names: List[str] = None) -> GameRead:
        rcrud = RoomCRUD(session=self.session)
        lcrud = LocationCRUD(session=self.session)

        # game.users = [str(game.host)]
        db_game = Game.model_validate(game)
        rcrud.get(game.room_id)
        self.session.add(db_game)
        self.session.commit()
        self.session.refresh(db_game)

        lcrud.create_all_game_rooms(game_id=db_game.id)

        self.populate_characters(id=db_game.id, character_names=character_names)

        self._deal_cards(game_id=db_game.id)

        self.set_turn(db_game.id, self.players(id=db_game.id)[0].id)

        return self.get(_id=db_game.id)

    def delete(self, _id: UUID) -> GameRead:
        game = self.session.get(Game, _id)
        if not game:
            raise HTTPException(status_code=404, detail="Hero not found")
        self.session.delete(game)
        self.session.commit()
        return True

    def update(self, _id: UUID, game: GameUpdate) -> GameRead:
        db_game = self.session.get(Game, _id)
        if not db_game:
            raise HTTPException(status_code=404, detail="Game not found")
        game_data = game.model_dump(exclude_unset=True)
        db_game.sqlmodel_update(game_data)
        self.session.add(db_game)
        self.session.commit()
        self.session.refresh(db_game)
        return db_game

    def add_player(self, _id: UUID, player_id: UUID) -> GameRead:
        game = self.get(_id=_id)

        new_game = GameUpdate(users=game.users)
        new_game.users.append(str(player_id))

        return self.update(_id=_id, game=new_game)

    def move_player(self, id: UUID, character_id: UUID, location_id: UUID, validate: bool = False):
        ccrud = CharacterCRUD(session=self.session)

        character = ccrud.get(character_id)
        character.location_id = location_id
        ccrud.update(character_id, )

    def set_win(self, id: UUID, game_over: bool) -> GameReadWithLinks:
        self.update(_id=id, game=GameUpdate(game_over=game_over))

        return self.get(id)

    def players(self, id: UUID) -> List[CharacterRead]:
        game = self.get(id)
        return [character for character in game.characters if character.is_playing]

    def set_turn(self, id: UUID, character_id: UUID) -> GameReadWithLinks:
        self.update(_id=id, game=GameUpdate(character_turn_id=character_id))

        # char_crud = CharacterCRUD(session=self.session)
        #
        # char_crud.update(CharacterUpdate(is_turn=True))

        return self.get(id)

    def increment_turn(self, id: UUID):
        game = self.get(id)

        next_player = self.get_next_player(id=id, current_player_id=game.character_turn_id)

        self.set_turn(id, next_player.id)

    def get_player_idx(self, id: UUID, current_player_id: UUID):
        for player_idx, player in enumerate(self.players(id)):
            if player.id == current_player_id:
                return player_idx

    def get_next_player(self, id: UUID, current_player_id: UUID) -> CharacterRead:

        from copy import deepcopy

        current_player_index = self.get_player_idx(id, current_player_id=current_player_id)

        players = self.players(id=id)
        in_order_players = players[current_player_index:]
        in_order_players.extend(players[:current_player_index])

        print("IN ORDER PLAYERS: ", in_order_players)

        for player in in_order_players:
            if player.id == current_player_id:
                continue

            return player
