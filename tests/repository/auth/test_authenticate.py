import pytest
from sqlalchemy.orm import Session

from app.api.errors import PasswordErrorException, UserNotExistsException
from app.api.v1.routes.auth.auth_repository import authenticate
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_authenticate(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    user_authenticate: User | None = authenticate(session=db_session, username=user.username, password=password)

    assert user_authenticate
    assert user_authenticate.username == user.username
    assert user_authenticate.email == user.email


def test_authenticate_with_username_error(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    with pytest.raises(UserNotExistsException):
        user_authenticate = authenticate(session=db_session, username=random_username(), password=user.password)



def test_authenticate_with_password_error(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    with pytest.raises(PasswordErrorException):
        user_authenticate = authenticate(session=db_session, username=user.username, password=random_lower_string())
