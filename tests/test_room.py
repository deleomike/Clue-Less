import uuid

import pytest
from fastapi.testclient import TestClient

from clueless.app.db.models.room import RoomCreate


def delete_room(app: TestClient, _id, headers):
    return app.delete(f"/api/room/{_id}", headers=headers)


def create_room(app: TestClient, create: RoomCreate, headers, delete: bool = True):
    response = app.post("/api/room", json=create, headers=headers)

    return response

    data = response.json()

    if delete:
        delete_room(app=app, _id=data["id"], headers=headers)


def test_create_room(test_client, test_user_a, test_user_a_header):
    create = {
        "name": "My-Room",
        "host": test_user_a.id
    }
    print("ROOM CREATE ", create)
    room = create_room(app=test_client, create=create, headers=test_user_a_header)

    if room.status_code == 401:
        pytest.fail("Unauthorized")

    if room.status_code != 200:
        print(room.json())
        pytest.fail(reason=f"Error {room.status_code}. {room.json()}")

    room = room.json()
    assert room["name"] == create["name"]
    assert room["host"] == test_user_a.id
    assert len(room["users"]) > 0

    assert test_user_a.id in room["users"]

    print(test_user_a)

    delete_room(app=test_client, _id=room["id"], headers=test_user_a_header)


@pytest.fixture
def user_a_room(test_client, test_user_a, test_user_a_header):
    create = {
        "name": "My-Room",
        "host": test_user_a.id
    }
    print("ROOM CREATE ", create)
    room = create_room(app=test_client, create=create, headers=test_user_a_header)

    room = room.json()

    yield room

    delete_room(app=test_client, _id=room["id"], headers=test_user_a_header)

def test_join(test_client, user_a_room, test_user_a, test_user_b, test_user_b_header):

    response = test_client.post(
        f"/api/room/{user_a_room['id']}/join",
        headers=test_user_b_header
    )

    room = response.json()

    assert test_user_b.id in room["users"]
    assert test_user_a.id in room["users"]
