import pytest
import concurrent

from clueless.app.db.models.room import RoomRead
from clueless.app.db.models.shared import GameReadWithLinks, CharacterReadLinks

from tests.game_utils import (
    get_character,
    start_game,
    move_character,
    valid_moves,
    make_suggestion,
    make_accusation,
    get_game,
    is_my_turn,
    get_solution
)



@pytest.fixture
def full_Room(test_client, user_a_room, test_user_a, test_user_b, test_user_b_header):
    response = test_client.post(
        f"/api/room/{user_a_room['id']}/join",
        headers=test_user_b_header
    )

    room = response.json()

    return room

@pytest.fixture
def game(test_client, full_Room, test_user_a_header) -> GameReadWithLinks:
    return start_game(room_id=full_Room["id"], test_client=test_client, headers=test_user_a_header)


@pytest.fixture()
def character_a(game, test_client, test_user_a_header):
    return get_character(
        game_id=game.id,
        test_client=test_client,
        headers=test_user_a_header
    )


@pytest.fixture()
def character_b(game, test_client, test_user_b_header):
    return get_character(
        game_id=game.id,
        test_client=test_client,
        headers=test_user_b_header
    )


def test_characters_unique(character_a, character_b):
    assert character_b.id != character_a.id


@pytest.fixture(scope="function")
def current_player_header(game, test_client, test_user_b_header, test_user_a_header):

    turn, _ = is_my_turn(game_id=game.id, test_client=test_client, headers=test_user_a_header)

    if turn:
        headers = test_user_a_header
    else:
        headers = test_user_b_header

    return headers


def test_start_game(test_client, full_Room, test_user_a_header):
    game = start_game(test_client=test_client, room_id=full_Room["id"], headers=test_user_a_header)

    assert str(game.room_id) == full_Room["id"]


def test_read_links(game):
    assert len(game.locations) > 0

    print("GAME: ", game)


def test_is_my_turn(test_client, game, test_user_a_header):
    turn, id = is_my_turn(game_id=game.id, test_client=test_client, headers=test_user_a_header)
    assert turn


def test_move_player(test_client, game, test_user_a_header, test_user_b_header, character_b):
    # turn, character_turn = is_my_turn(game_id=game.id, test_client=test_client, headers=test_user_a_header)

    print("=============================")
    turn, character_turn = is_my_turn(game_id=game.id, test_client=test_client, headers=test_user_b_header)
    print("B: ", turn, character_b.id)
    turn, character_turn = is_my_turn(game_id=game.id, test_client=test_client, headers=test_user_a_header)
    print("A: ", turn, get_character(game_id=game.id, test_client=test_client, headers=test_user_a_header).id)
    print("=============================")
    if turn:
        headers = test_user_a_header
    else:
        headers = test_user_b_header

    locations = valid_moves(
        game_id=game.id,
        test_client=test_client,
        headers=headers
    )

    first_location_id = locations[0].id

    character = move_character(
        game_id=game.id,
        test_client=test_client,
        headers=headers,
        location_id=first_location_id
    )

    assert character.location_id == first_location_id


def test_suggestion(test_client, game, current_player_header, character_b):
    turn, _ = is_my_turn(game_id=game.id, test_client=test_client, headers=current_player_header)

    assert turn

    locations = valid_moves(
        game_id=game.id,
        test_client=test_client,
        headers=current_player_header
    )

    for location in locations:
        if "-" not in location.name:
            location_id = location.id
            break

    character = move_character(
        game_id=game.id,
        test_client=test_client,
        headers=current_player_header,
        location_id=location_id
    )

    assert character.location_id == location_id

    response = make_suggestion(
        game_id=game.id,
        character_name="Col. Mustard",
        weapon_name="dagger",
        test_client=test_client,
        headers=current_player_header
    )
    print("CARD: ", response)


def test_accusation(test_client, game, current_player_header, character_b):

    win = make_accusation(
        game_id=game.id,
        headers=current_player_header,
        weapon_name="candlestick",
        room_name="study",
        character_name=character_b.name,
        test_client=test_client
    )

def test_correct_answer(test_client, game, test_user_a_header):
    solution = get_solution(game_id=game.id, test_client=test_client, headers=test_user_a_header)

    win = make_accusation(
        game_id=game.id,
        headers=test_user_a_header,
        weapon_name=solution["weapon"],
        room_name=solution["room"],
        character_name=solution["character"],
        test_client=test_client
    )

    assert win


def test_overload(test_client, game, test_user_a_header):
    # concurrent.futures
    # with concurrent.futures.ThreadPoolExecutor() as executor:  # optimally defined number of threads
    #     res = [executor.submit(get_game, game.id, test_client, test_user_a_header) for _ in range(100000)]
    #     concurrent.futures.wait(res)
    for _ in range(100):
        get_character(game_id=game.id, test_client=test_client, headers=test_user_a_header)
        get_game(game_id=game.id, test_client=test_client, headers=test_user_a_header)






