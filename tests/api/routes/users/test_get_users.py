from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_get_users_with_admin_user_auth(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users/",
                   headers=admin_user_token_headers)

    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) > 1
    for user in all_users:
        assert "username" in user
        assert "password" in user
        assert "email" in user


def test_get_users_with_normal_user_auth(client: TestClient, db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users/",
                   headers=test_user_token_headers)

    all_users = r.json()

    assert r.status_code == 403
    assert all_users["message"] == "The user doesn't have enough privileges"


def test_get_users_with_error_query_skip(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users?skip=De",
                   headers=admin_user_token_headers)

    assert r.status_code == 422


def test_get_users_with_error_query_limit(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users?limit=De",
                   headers=admin_user_token_headers)

    assert r.status_code == 422


def test_get_users_with_query_limit(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users?limit=10",
                   headers=admin_user_token_headers)

    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) > 1
    for user in all_users:
        assert "username" in user
        assert "password" in user
        assert "email" in user


def test_get_users_with_query_skip(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users?skip=2",
                   headers=admin_user_token_headers)

    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) == 1
    for user in all_users:
        assert "username" in user
        assert "password" in user
        assert "email" in user


def test_get_users_with_query_skip_and_limit(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    r = client.get(f"{settings.API_V1_STR}/users?skip=0&limit=10",
                   headers=admin_user_token_headers)

    all_users = r.json()

    assert r.status_code == 200
    assert len(all_users) > 1
    for user in all_users:
        assert "username" in user
        assert "password" in user
        assert "email" in user
