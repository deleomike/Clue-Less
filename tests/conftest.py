import pydantic
import pytest
import uuid

from typing import Dict
from fastapi.testclient import TestClient

from clueless.app.webapp import app
from clueless.app.db.user_schemas import UserCreate, UserLogin


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