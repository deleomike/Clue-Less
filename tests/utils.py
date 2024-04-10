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