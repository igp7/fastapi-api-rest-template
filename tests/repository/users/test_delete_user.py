from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import delete_user
from app.database.models.user import User
from tests.utils.user import create_new_user
from tests.utils.utils import random_email, random_lower_string, random_username


def test_delete_user_with_user_valid(db_session: Session) -> None:
    username: str = random_username()
    password: str = random_lower_string()
    email: str = random_email()

    user: User = create_new_user(db_session=db_session, username=username, password=password, email=email)

    delete_user(session=db_session, user=user)

    statement = select(User).where(User.username == username)
    user = db_session.execute(statement).scalar_one_or_none()

    assert user is None
