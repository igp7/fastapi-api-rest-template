from fastapi.testclient import TestClient

from app.config import settings
from app.database.models.user import User
from tests.utils.utils import random_email, random_lower_string, random_username


def test_create_new_user(client: TestClient) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    data: dict[str:str] = {"username": username, "email": email, "password": password}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    created_user = r.json()

    assert r.status_code == 201
    assert created_user["username"] == settings.TEST_NORMAL_USER_USERNAME
    assert created_user["email"] == settings.TEST_NORMAL_USER_EMAIL


def test_create_user_with_existing_username(client: TestClient, test_user: User) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    data: dict[str:str] = {"username": username, "password": password, "email": email}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "The user with this data already exists in the system."


def test_create_user_with_existing_email(client: TestClient, test_user: User) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    data: dict[str:str] = {"username": username, "password": password, "email": email}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "The user with this data already exists in the system."


def test_create_user_without_email(client: TestClient) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    data: dict[str:str] = {"username": username, "password": password}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    assert r.status_code == 422


def test_create_user_without_username(client: TestClient) -> None:
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    data: dict[str:str] = {"email": email, "password": password}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    assert r.status_code == 422


def test_create_user_without_password(client: TestClient) -> None:
    email: str = settings.TEST_NORMAL_USER_EMAIL
    username: str = settings.TEST_NORMAL_USER_USERNAME

    data: dict[str:str] = {"email": email, "username": username}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )

    assert r.status_code == 422


def test_create_new_user_with_auth_headers(client: TestClient, admin_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    email: str = random_email()
    password: str = random_lower_string()
    data: dict[str:str] = {"username": username, "email": email, "password": password}

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
        headers=admin_user_token_headers,
    )

    created_user = r.json()

    assert r.status_code == 201
    assert created_user["username"] == username
    assert created_user["email"] == email
