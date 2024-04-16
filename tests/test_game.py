import pytest

from clueless.app.db.models.room import RoomRead



@pytest.fixture
def full_Room(test_client, user_a_room, test_user_a, test_user_b, test_user_b_header):
    response = test_client.post(
        f"/api/room/{user_a_room['id']}/join",
        headers=test_user_b_header
    )

    room = response.json()

    return room

@pytest.fixture
def game(test_client, full_Room, test_user_a_header):
    response = test_client.post(
        f"/api/room/{full_Room['id']}/start",
        headers=test_user_a_header
    ).json()

    return response


@pytest.fixture()
def character_b(game, test_client, test_user_b_header):
    response = test_client.get(
        f"/api/game/{game['id']}/character/",
        headers=test_user_b_header
    ).json()

    return response


def test_start_game(test_client, full_Room, test_user_a_header):
    response = test_client.post(
        f"/api/room/{full_Room['id']}/start",
        headers=test_user_a_header
    ).json()

    assert response["room_id"] == full_Room["id"]


def test_read_links(game):
    assert len(game["locations"]) > 0

    print("GAME: ", game)


def test_move_player(test_client, game, test_user_a_header):
    response = test_client.post(
        f"/api/game/{game['id']}/character/valid_moves",
        headers=test_user_a_header
    ).json()

    first_location_id = response[0]["id"]

    response = test_client.post(
        f"/api/game/{game['id']}/character/move/{first_location_id}",
        headers=test_user_a_header
    ).json()

    assert response["location_id"] == first_location_id


def test_suggestion(test_client, game, test_user_a_header, character_b):
    response = test_client.post(
        f"/api/game/{game['id']}/character/valid_moves",
        headers=test_user_a_header
    ).json()

    for location in response:
        if "-" not in location["name"]:
            location_id = location["id"]
            break

    response = test_client.post(
        f"/api/game/{game['id']}/character/move/{location_id}",
        headers=test_user_a_header
    ).json()

    assert response["location_id"] == location_id

    response = test_client.post(
        f"/api/game/{game['id']}/character/make_suggestion",
        headers=test_user_a_header,
        json={
            "accused_player_id": character_b["id"],
            "weapon": "candlestick",
        }
    ).json()

    print(response)


def test_accusation(test_client, game, test_user_a_header, character_b):
    response = test_client.post(
        f"/api/game/{game['id']}/character/valid_moves",
        headers=test_user_a_header
    ).json()

    for location in response:
        if "-" not in location["name"]:
            location_id = location["id"]
            break

    response = test_client.post(
        f"/api/game/{game['id']}/character/move/{location_id}",
        headers=test_user_a_header
    ).json()

    assert response["location_id"] == location_id

    response = test_client.post(
        f"/api/game/{game['id']}/character/make_accusation",
        headers=test_user_a_header,
        json={
            "accused_player_id": character_b["id"],
            "character": character_b["name"],
            "room": location["name"],
            "weapon": "candlestick",
        }
    ).json()

    print(response)








