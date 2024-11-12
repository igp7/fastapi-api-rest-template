from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_delete_user_by_username_with_admin_user_auth(client: TestClient, db_session: Session, admin_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    r = client.delete(f"{settings.API_V1_STR}/users/{username}",
                      headers=admin_user_token_headers)

    current_user = r.json()

    assert current_user["message"] == f"The user with username {username} delete in the system."


def test_delete_user_by_username_with_normal_user_auth(client: TestClient, db_session: Session, test_user_token_headers: dict[str, str]) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    r = client.delete(f"{settings.API_V1_STR}/users/{username}",
                      headers=test_user_token_headers)

    current_user = r.json()

    assert r.status_code == 403
    assert current_user["message"] == "The user doesn't have enough privileges"


def test_get_user_by_username_without_user_auth(client: TestClient, db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    r = client.delete(f"{settings.API_V1_STR}/users/{username}")

    response_data = r.json()

    assert r.status_code == 401
    assert response_data["detail"] == "Not authenticated"
