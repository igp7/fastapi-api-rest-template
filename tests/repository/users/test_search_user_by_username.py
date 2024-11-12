from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import search_user_by_username
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_search_user_by_username_with_username_valid(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    user_search: User = search_user_by_username(session=db_session, username=user.username)

    assert user.email == user_search.email
    assert user.username == user_search.username


def test_search_user_by_username_with_username_not_valid(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    user_search: User = search_user_by_username(session=db_session, username=random_username())

    assert user_search is None
