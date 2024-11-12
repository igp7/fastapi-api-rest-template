from fastapi.testclient import TestClient

from app.config import settings


def test_delete_user_me_with_admin_user_auth(client: TestClient, admin_user_token_headers: dict[str, str]) -> None:
    r = client.delete(f"{settings.API_V1_STR}/users/me",
                      headers=admin_user_token_headers)

    current_user = r.json()

    assert current_user["message"] == f"The user with username {settings.TEST_ADMIN_USER_USERNAME} delete in the system."


def test_delete_user_me_with_normal_user_auth(client: TestClient, test_user_token_headers: dict[str, str]) -> None:
    r = client.delete(f"{settings.API_V1_STR}/users/me",
                      headers=test_user_token_headers)

    current_user = r.json()

    assert current_user["message"] == f"The user with username {settings.TEST_NORMAL_USER_USERNAME} delete in the system."


def test_get_user_me_without_user_auth(client: TestClient) -> None:
    r = client.delete(f"{settings.API_V1_STR}/users/me")

    response_data = r.json()

    assert r.status_code == 401
    assert response_data["detail"] == "Not authenticated"
