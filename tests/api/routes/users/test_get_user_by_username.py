from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_username


def test_get_existing_user_by_username(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD

    user_existing: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_existing.username}",
        headers=admin_user_token_headers,
    )

    response_data = r.json()

    assert r.status_code == 200
    assert response_data["username"] == user_existing.username
    assert response_data["email"] == user_existing.email


def test_get_admin_user_by_username(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = settings.TEST_ADMIN_USER_USERNAME

    r = client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=admin_user_token_headers,
    )

    response_data = r.json()

    assert r.status_code == 200
    assert response_data["username"] == settings.TEST_ADMIN_USER_USERNAME
    assert response_data["email"] == settings.TEST_ADMIN_USER_EMAIL


def test_get_existing_user_permissions_error(client: TestClient, test_user_token_headers: dict[str:str]) -> None:
    username_random: str = random_username()

    r = client.get(
        f"{settings.API_V1_STR}/users/{username_random}",
        headers=test_user_token_headers,
    )

    response_data = r.json()

    assert r.status_code == 403
    assert response_data["message"] == "The user doesn't have enough privileges"


def test_get_not_existing_user_permissions_error(client: TestClient, admin_user_token_headers: dict[str:str]) -> None:
    username_random: str = random_username()

    r = client.get(
        f"{settings.API_V1_STR}/users/{username_random}",
        headers=admin_user_token_headers,
    )

    response_data = r.json()

    assert r.status_code == 404
    assert response_data["message"] == "User not found."
