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


def test_start_game(test_client, full_Room, test_user_a_header):
    response = test_client.post(
        f"/api/room/{full_Room['id']}/start",
        headers=test_user_a_header
    ).json()

    assert response["room_id"] == full_Room["id"]


def test_read_links(game):
    assert len(game["locations"]) > 0

    print("GAME: ", game)