import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.errors import EmailExistsException, UsernameExistsException
from app.api.v1.routes.users.users_repository import create_user
from app.api.v1.routes.users.users_schemas import UserCreateSchema
from app.config import settings
from app.database.models.user import User
from tests.utils.utils import random_email, random_username


def test_create_new_user(db_session: Session) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    data: dict[str:str] = {"username": username, "email": email, "password": password}

    created_user: User = create_user(session=db_session, user=UserCreateSchema(**data), is_admin=False)

    assert created_user.username == settings.TEST_NORMAL_USER_USERNAME
    assert created_user.email == settings.TEST_NORMAL_USER_EMAIL

    statement = select(User).where(User.username == username)
    user_db: User = db_session.execute(statement).scalar_one_or_none()

    assert user_db.username == settings.TEST_NORMAL_USER_USERNAME
    assert user_db.email == settings.TEST_NORMAL_USER_EMAIL


def test_create_user_with_existing_username(db_session: Session) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    data_user_1: dict[str:str] = {"username": username, "email": email, "password": password}
    data_user_2: dict[str:str] = {"username": username, "email": random_email(), "password": password}

    created_user_1: User = create_user(session=db_session, user=UserCreateSchema(**data_user_1), is_admin=False)

    with pytest.raises(UsernameExistsException):
        created_user_2 = create_user(session=db_session, user=UserCreateSchema(**data_user_2), is_admin=False)



def test_create_user_with_existing_email(db_session: Session) -> None:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    email: str = settings.TEST_NORMAL_USER_EMAIL
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    data_user_1: dict[str:str] = {"username": username, "email": email, "password": password}
    data_user_2: dict[str:str] = {"username": random_username(), "email": email, "password": password}

    created_user_1: User = create_user(session=db_session, user=UserCreateSchema(**data_user_1), is_admin=False)

    with pytest.raises(EmailExistsException):
        created_user_2 = create_user(session=db_session, user=UserCreateSchema(**data_user_2), is_admin=False)
