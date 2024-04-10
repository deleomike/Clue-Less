import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationCreate
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate, GameReadWithLinks
from clueless.app.db.crud.character import CharacterCRUD, CharacterCreate


class GameCRUD(BaseCRUD):

    DEFAULT_NAMES = ["Prof. Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White", "Col. Mustard", "Miss Scarlet"]

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
            character_names = self.DEFAULT_NAMES[:len(game.waiting_room.users)]

        assert (len(game.waiting_room.users) == len(character_names))

        starting_location = game.locations[0]
        for user, name in zip(game.waiting_room.users, character_names):
            create = CharacterCreate(
                name=name,
                user_id=user,
                location_id=starting_location.id,
                game_id=game.id
            )

            ccrud.create(character=create)

        return self.get(id)

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