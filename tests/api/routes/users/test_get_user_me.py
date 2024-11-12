from fastapi.testclient import TestClient

from app.config import settings


def test_get_user_me_with_admin_user_auth(client: TestClient, admin_user_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me",
                   headers=admin_user_token_headers)

    current_user = r.json()

    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_admin"]
    assert current_user["email"] == settings.TEST_ADMIN_USER_EMAIL
    assert current_user["username"] == settings.TEST_ADMIN_USER_USERNAME


def test_get_user_me_with_normal_user_auth(client: TestClient, test_user_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me",
                   headers=test_user_token_headers)

    current_user = r.json()

    assert r.status_code == 200
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_admin"] is False
    assert current_user["email"] == settings.TEST_NORMAL_USER_EMAIL
    assert current_user["username"] == settings.TEST_NORMAL_USER_USERNAME


def test_get_user_me_without_user_auth(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me")

    response_data = r.json()

    assert r.status_code == 401
    assert response_data["detail"] == "Not authenticated"
