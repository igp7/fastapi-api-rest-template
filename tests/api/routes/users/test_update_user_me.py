from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_update_user_me(client: TestClient, db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    new_username: str = "Updated Name"
    email: str = random_email()
    data: dict[str:str] = {"username": new_username, "email": email}

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=test_user_token_headers,
        json=data,
    )

    updated_user = r.json()
    assert r.status_code == 200
    assert updated_user["email"] == email
    assert updated_user["username"] == new_username

    statement = select(User).where(User.username == new_username)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.email == email
    assert user_db.username == new_username


def test_update_user_me_with_new_username(client: TestClient, db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    new_username: str = "Updated Name"
    data: dict[str:str] = {"username": new_username}

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=test_user_token_headers,
        json=data,
    )

    updated_user = r.json()
    assert r.status_code == 200
    assert updated_user["username"] == new_username

    statement = select(User).where(User.username == new_username)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.username == new_username


def test_update_user_me_with_new_email(client: TestClient, db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    new_email: str = random_email()
    data: dict[str:str] = {"email": new_email}

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=test_user_token_headers,
        json=data,
    )

    updated_user = r.json()
    assert r.status_code == 200
    assert updated_user["email"] == new_email

    statement = select(User).where(User.email == new_email)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.email == new_email


def test_update_user_me_with_email_exists(client: TestClient,  db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)
    data: dict[str:str] = {"email": user.email}

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=test_user_token_headers,
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "User with this email already exists."


def test_update_user_me_with_username_exists(client: TestClient,  db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)
    data: dict[str:str] = {"username": user.username}

    r = client.put(
        f"{settings.API_V1_STR}/users/me",
        headers=test_user_token_headers,
        json=data,
    )

    response_data = r.json()

    assert r.status_code == 409
    assert response_data["message"] == "The user with this username already exists in the system."
