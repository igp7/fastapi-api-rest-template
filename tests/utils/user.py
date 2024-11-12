from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import create_user
from app.api.v1.routes.users.users_schemas import UserCreateSchema
from app.config import settings
from app.database.models.user import User


def create_new_user(*, db_session: Session, username: str, password: str, email: str, is_admin: bool = False) -> User:
    user_in = UserCreateSchema(username=username, email=email, password=password)
    user = create_user(session=db_session, user=user_in, is_admin=is_admin)

    return user


def get_user_token_headers(*, client: TestClient, username: str, password: str) -> dict[str, str]:
    data = {"username": username,
            "password": password}

    r = client.post(f"{settings.API_V1_STR}/login", data=data)
    response = r.json()

    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers
