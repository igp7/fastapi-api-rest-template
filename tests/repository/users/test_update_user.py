import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.errors import EmailExistsException, UsernameExistsException
from app.api.v1.routes.users.users_repository import update_user
from app.api.v1.routes.users.users_schemas import UserUpdateSchema
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_update_user_with_new_username(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_username: str = random_username()
    data: dict[str:str] = {"username": new_username}

    updated_user = update_user(session=db_session, user=user_1, new_data_user=UserUpdateSchema(**data))

    assert updated_user.username == new_username
    assert updated_user.email == email

    statement = select(User).where(User.username == new_username)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.username == new_username


def test_update_user_with_new_email(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_email: str = random_email()
    data: dict[str:str] = {"email": new_email}

    updated_user = update_user(session=db_session, user=user_1, new_data_user=UserUpdateSchema(**data))

    assert updated_user.username == username
    assert updated_user.email == new_email

    statement = select(User).where(User.email == new_email)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.email == new_email


def test_update_user_with_username_exit(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    data: dict[str:str] = {"username": username_1}

    with pytest.raises(UsernameExistsException):
        updated_user = update_user(session=db_session, user=user_2, new_data_user=UserUpdateSchema(**data))


def test_update_user_with_email_exit(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    data: dict[str:str] = {"email": email_1}

    with pytest.raises(EmailExistsException):
        updated_user = update_user(session=db_session, user=user_2, new_data_user=UserUpdateSchema(**data))


def test_update_user_with_new_password(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_password: str = random_lower_string()
    data: dict[str:str] = {"password": new_password}

    updated_user: User = update_user(session=db_session, user=user_1, new_data_user=UserUpdateSchema(**data))

    assert updated_user.username == username
    assert updated_user.email == email

    statement = select(User).where(User.username == username)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.username == username


def test_update_user_with_new_email_and_new_username(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    new_email: str = random_email()
    new_username: str = random_username()
    data: dict[str:str] = {"username": new_username, "email": new_email}

    updated_user: User = update_user(session=db_session, user=user_1, new_data_user=UserUpdateSchema(**data))

    assert updated_user.username == new_username
    assert updated_user.email == new_email

    statement = select(User).where(User.username == new_username)
    user_db = db_session.execute(statement).scalar_one_or_none()

    assert user_db
    assert user_db.username == new_username
    assert user_db.email == new_email
