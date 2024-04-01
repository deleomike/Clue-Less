import uuid

from sqlmodel import select
from typing import List, Union
from uuid import UUID
from fastapi import HTTPException

from clueless.app.db.crud.base import BaseCRUD
from clueless.app.db.crud.room import RoomCRUD
from clueless.app.db.crud.location import LocationCRUD, LocationCreate
from clueless.app.db.models.game import GameBase, Game, GameRead, GameCreate, GameUpdate, GameReadWithLinks


class GameCRUD(BaseCRUD):

    def get(self, _id: UUID) -> GameReadWithLinks:
        game = self.session.get(Game, _id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    def get_all(self) -> List[GameRead]:
        games = self.session.exec(select(Game)).all()
        return games

    def create(self, game: GameCreate) -> GameRead:
        rcrud = RoomCRUD(session=self.session)
        lcrud = LocationCRUD(session=self.session)

        # game.users = [str(game.host)]
        db_game = Game.model_validate(game)
        rcrud.get(game.room_id)
        self.session.add(db_game)
        self.session.commit()
        self.session.refresh(db_game)

        location_names = [
            "study",
            "hall",
            "lounge",
            "dining_room",
            "billiard_room",
            "library",
            "conservatory",
            "ball_room",
            "kitchen"
        ]

        for name in location_names:
            create = LocationCreate(game_id=db_game.id, name=name)
            lcrud.create(location=create)

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
