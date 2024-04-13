import pydantic
import pytest
import uuid
import asyncio

from typing import Dict
from fastapi.testclient import TestClient

from tests.utils import create_room, delete_room

from clueless.app.webapp import app
from clueless.app.db.user_schemas import UserCreate, UserLogin

from clueless.app.db import create_db_and_tables, alchemy_create_db_and_tables

async def setup():
    create_db_and_tables()
    await alchemy_create_db_and_tables()

asyncio.run(setup())

class User(pydantic.BaseModel):
    id: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

@pytest.fixture
def test_client():
    return TestClient(app)


def delete_user(app: TestClient, _id: uuid.uuid4):
    return app.delete(f"/api/users/{_id}")


def create_user(app: TestClient, create: UserCreate):
    response = app.post("/api/auth/register", data=create.json())
    return response


@pytest.fixture
def test_user_a(test_client) -> UserCreate:
    email = f"testa-{uuid.uuid4()}@google.com".replace("-", "")
    password = "password"
    create = UserCreate(
        email=email,
        password=password
    )
    response = create_user(app=test_client, create=create)

    print("CREATE USER RESPONSE ", response.json())

    user = response.json()
    user["password"] = password

    yield User(**user)


@pytest.fixture
def test_user_b(test_client) -> UserCreate:
    email = f"testb-{uuid.uuid4()}@google.com".replace("-", "")
    password = "password"
    create = UserCreate(
        email=email,
        password=password
    )
    response = create_user(app=test_client, create=create)

    print("CREATE USER RESPONSE ", response.json())

    user = response.json()
    user["password"] = password

    yield User(**user)


def get_user_headers(app: TestClient, email: str, password: str):
    payload = {
        "username": email,
        "password": password
    }
    # payload = f"?grant_type=&username={email}&password={password}&scope=&client_id=&client_secret="
    print("LOGIN PAYLOAD ", payload)
    login = app.post(f"/api/auth/jwt/login", data=payload).json()

    print("LOGIN ", login)

    headers = {
        'Authorization': f'Bearer {login["access_token"]}',
    }

    return headers

@pytest.fixture
def test_user_a_header(test_client, test_user_a) -> Dict:
    return get_user_headers(app=test_client, email=test_user_a.email, password=test_user_a.password)


@pytest.fixture
def test_user_b_header(test_client, test_user_b) -> Dict:
    return get_user_headers(app=test_client, email=test_user_b.email, password=test_user_b.password)


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