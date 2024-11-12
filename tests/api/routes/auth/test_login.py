from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.user import User
from tests.utils.user import create_new_user


def test_login_successful(client: TestClient, db_session: Session) -> None:
    username: str = settings.TEST_ADMIN_USER_USERNAME
    password: str = settings.TEST_ADMIN_USER_PASSWORD
    email: str = settings.TEST_ADMIN_USER_EMAIL

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    login_data: dict[str:str] = {
        "username": username,
        "password": password,
    }

    r = client.post(f"{settings.API_V1_STR}/login",
                    data=login_data)

    response = r.json()

    assert r.status_code == 200
    assert "access_token" in response
    assert response["access_token"]
    assert "token_type" in response
    assert response["token_type"] == "bearer"


def test_login_with_incorrect_password(client: TestClient) -> None:
    login_data: dict[str:str] = {
        "username": settings.TEST_ADMIN_USER_USERNAME,
        "password": "incorrect",
    }

    r = client.post(f"{settings.API_V1_STR}/login",
                    data=login_data)

    response = r.json()

    assert r.status_code == 400
    assert response["message"] == "Incorrect username or password"


def test_login_with_incorrect_username(client: TestClient) -> None:
    login_data: dict[str:str] = {
        "username": "test_user",
        "password": settings.TEST_ADMIN_USER_PASSWORD,
    }

    r = client.post(f"{settings.API_V1_STR}/login",
                    data=login_data)

    response = r.json()

    assert r.status_code == 400
    assert response["message"] == "Incorrect username or password"


def test_login_with_access_token_headers(client: TestClient, admin_user_token_headers: dict[str, str]) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login",
        headers=admin_user_token_headers,
    )

    assert r.status_code == 422
