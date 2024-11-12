from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import search_users
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_search_users_without_query_params(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2 = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users = search_users(session=db_session)

    assert len(users) >= 2
    for user in users:
        assert user.username
        assert user.password
        assert user.email


def test_get_users_whit_negative_query_skip(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2 = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users = search_users(session=db_session, skip=-2)

    assert len(users) >= 2
    for user in users:
        assert user.username
        assert user.password
        assert user.email


def test_get_users_whit_negative_query_limit(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2 = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users = search_users(session=db_session, limit=-2)

    assert len(users) >= 2
    for user in users:
        assert user.username
        assert user.password
        assert user.email


def test_get_users_whit_query_limit(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1 = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2 = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users = search_users(session=db_session, limit=10)

    assert len(users) >= 2
    for user in users:
        assert user.username
        assert user.password
        assert user.email


def test_get_users_whit_query_skip(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users: Sequence[User] = search_users(session=db_session, skip=1)

    assert len(users) == 1
    for user in users:
        assert user.username
        assert user.password
        assert user.email


def test_get_users_whit_query_skip_and_limit(db_session: Session) -> None:
    username_1: str = random_username()
    password_1: str = random_lower_string()
    email_1: str = random_email()

    username_2: str = random_username()
    password_2: str = random_lower_string()
    email_2: str = random_email()

    user_1: User = create_new_user(db_session=db_session, username=username_1, password=password_1, email=email_1)
    user_2: User = create_new_user(db_session=db_session, username=username_2, password=password_2, email=email_2)

    users: Sequence[User] = search_users(session=db_session, skip=0, limit=10)

    assert len(users) >= 2
    for user in users:
        assert user.username
        assert user.password
        assert user.email
