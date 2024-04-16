import click
import asyncio

from typing import List

from clueless.app.db.user_schemas import UserRead
from clueless.app.core.users import create_user, get_user_manager, fastapi_users, get_user
from clueless.app.db.crud.room import RoomCRUD, Room, RoomCreate, RoomRead, RoomUpdate
from clueless.app.db.crud.game import GameCRUD, GameRead, GameCreate


class RoomBuilder:
    """
    Builds the room, and gets the user credentials
    """

    def __init__(self, num_players, session, dummy_data: bool = False):
        self.num_players = num_players
        self.dummy_data = dummy_data
        self.players: List[UserRead] = []

        self.room_crud = RoomCRUD(session=session)
        self.game_crud = GameCRUD(session=session)



    def _create_or_login(self, username, password):
        user = asyncio.run(create_user(email=username, password=password))

        if user is None:
            # user_manager = asyncio.run(anext(get_user_manager()))
            user = asyncio.run(get_user(email=username))
            # user_manager = asyncio.run(anext(fastapi_users.get_user_manager()))
            # return asyncio.run(user_manager.get_by_email(user_email=username))
            # return asyncio.run(fastapi_users.get_user_manager()).get_by_email(user_email=username)
        return user

    def _prompt_user(self) -> UserRead:
        """
        Logs in or registers the user. Attempts the login, if that is not good, it registers them

        :return:
        """
        username = click.prompt("Email: ", type=str)
        password = click.prompt("Password: ", type=str)

        return self._create_or_login(username, password)

    def _create_users_(self):
        for num in range(self.num_players):
            if self.dummy_data:
                email = f"player{num}@clue.com"
                password = "password"
                self.players.append(self._create_or_login(username=email, password=password))
            else:
                self.players.append(self._prompt_user())

    def create_room_and_start(self, name: str = "My Room") -> GameRead:

        self._create_users_()

        create = RoomCreate(
            name=name,
            player_limit=self.num_players,
            host=self.players[0].id
        )

        room = self.room_crud.create(room=create)

        for idx, player in enumerate(self.players):
            if idx == 0:
                continue
            self.room_crud.add_player(_id=room.id, player_id=player.id)

        room = self.room_crud.get(room.id)

        create = GameCreate(room_id=room.id)

        game = self.game_crud.create(game=create)

        self.room_crud.update(_id=room.id, room=RoomUpdate(is_started=True))

        return game
