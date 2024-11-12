from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import search_user_by_username
from app.config import settings
from app.database.base import Base
from app.database.models.user import User
from app.database.session import engine
from app.main import app
from tests.utils.user import create_new_user, get_user_token_headers


@pytest.fixture(scope="function", autouse=True, name="db_session")
def db_session_fixture() -> Generator[Session, None, None]:
    with Session(engine) as session:
        Base.metadata.create_all(bind=engine)
        yield session
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module", name="client")
def client_fixture() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function", name="admin_user_token_headers")
def admin_user_token_headers_fixture(client: TestClient, db_session: Session) -> dict[str, str]:
    username = settings.TEST_ADMIN_USER_USERNAME
    password = settings.TEST_ADMIN_USER_PASSWORD
    email = settings.TEST_ADMIN_USER_EMAIL

    user = search_user_by_username(session=db_session, username=username)

    if not user:
        user = create_new_user(db_session=db_session,
                               username=username,
                               password=password,
                               email=email,
                               is_admin=True)

    return get_user_token_headers(client=client,
                                  username=username,
                                  password=password)


@pytest.fixture(scope="function", name="test_user_token_headers")
def test_user_token_headers_fixture(client: TestClient, db_session: Session) -> dict[str, str]:
    username = settings.TEST_NORMAL_USER_USERNAME
    password = settings.TEST_NORMAL_USER_PASSWORD
    email = settings.TEST_NORMAL_USER_EMAIL

    user = search_user_by_username(session=db_session, username=username)

    if not user:
        user = create_new_user(db_session=db_session,
                               username=username,
                               password=password,
                               email=email,
                               is_admin=False)

    return get_user_token_headers(client=client,
                                  username=settings.TEST_NORMAL_USER_USERNAME,
                                  password=settings.TEST_NORMAL_USER_PASSWORD)


@pytest.fixture(scope="function", name="test_user")
def test_user_fixture(client: TestClient, db_session: Session) -> User:
    username: str = settings.TEST_NORMAL_USER_USERNAME
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    email: str = settings.TEST_NORMAL_USER_EMAIL

    user = search_user_by_username(session=db_session, username=username)

    if not user:
        user = create_new_user(db_session=db_session,
                           username=username,
                           password=password,
                           email=email)

    return user


@pytest.fixture(scope="function", name="admin_user")
def admin_user_fixture(client: TestClient, db_session: Session) -> User:
    username: str = settings.TEST_ADMIN_USER_USERNAME
    password: str = settings.TEST_ADMIN_USER_PASSWORD
    email: str = settings.TEST_ADMIN_USER_EMAIL

    user = search_user_by_username(session=db_session, username=username)

    if not user:
        user = create_new_user(db_session=db_session,
                               username=username,
                               password=password,
                               email=email)

    return user
