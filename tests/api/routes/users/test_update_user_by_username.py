from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_update_user_by_username(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_username: str = random_username()
    data: dict[str:str] = {"username": new_username}

    r = client.put(
        f"{settings.API_V1_STR}/users/{user_1.username}",
        headers=admin_user_token_headers,
        json=data,
    )

    updated_user = r.json()

    assert r.status_code == 200
    assert updated_user["email"] == email


def test_update_user_by_username_with_new_username(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    email: str = settings.TEST_NORMAL_USER_EMAIL

    user_1: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_username: str = "Updated Name"
    data: dict[str:str] = {"username": new_username}

    r = client.put(
        f"{settings.API_V1_STR}/users/{user_1.username}",
        headers=admin_user_token_headers,
        json=data,
    )

    updated_user = r.json()
    assert r.status_code == 200
    assert updated_user["username"] == new_username


def test_update_user_by_username_with_new_email(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    email: str = settings.TEST_NORMAL_USER_EMAIL

    user_1: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_email: str = random_email()
    data: dict[str:str] = {"email": new_email}

    r = client.put(
        f"{settings.API_V1_STR}/users/{user_1.username}",
        headers=admin_user_token_headers,
        json=data,
    )

    updated_user = r.json()
    assert r.status_code == 200
    assert updated_user["email"] == new_email


def test_update_user_by_username_with_email_exists(client: TestClient,  db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    data: dict[str:str] = {"email": user_1.email}

    r = client.put(
        f"{settings.API_V1_STR}/users/{user_2.username}",
        headers=admin_user_token_headers,
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "User with this email already exists."


def test_update_user_by_username_with_username_exists(client: TestClient,  db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    data: dict[str:str] = {"username": user_1.username}

    r = client.put(
        f"{settings.API_V1_STR}/users/{user_2.username}",
        headers=admin_user_token_headers,
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "The user with this username already exists in the system."
