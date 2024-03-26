import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate


class GameCRUD(BaseCRUD):

    def get_by_id_or_key(self, _id: Union[str, UUID]) -> GameRead:
        """
        Gets the game by either the alphanumeric game key or by the ID
        :param _id:
        :return:
        """
        # try string to UUID conversion
        if isinstance(_id, str):
            try:
                uuid_obj = UUID(_id)
                _id = uuid_obj
            except ValueError:
                pass

        # Get game by uuid
        if isinstance(_id, UUID):
            return self.get(_id=_id)
        # Get game by game_key
        elif isinstance(_id, str):
            return self.get_by_game_key(game_key=_id)
        # Invalid ID
        else:
            raise HTTPException(status_code=500, detail=f"Invalid type for id, {type(_id)}")

    def get(self, _id: UUID) -> GameRead:
        game = self.session.get(Game, _id)
        if not game:
            raise HTTPException(status_code=404, detail="Hero not found")
        return game

    def get_all(self) -> List[GameRead]:
        games = self.session.exec(select(Game)).all()
        return games

    def create(self, game: GameCreate) -> GameRead:
        rcrud = RoomCRUD(session=self.session)

        # game.users = [str(game.host)]
        db_game = Game.model_validate(game)
        rcrud.get(game.room_id)
        self.session.add(db_game)
        self.session.commit()
        self.session.refresh(db_game)

        return db_game

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
