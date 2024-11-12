from collections.abc import Generator

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.api.errors import (
    InactiveUserException,
    InvalidTokenException,
    UnauthorizedException,
    UserNotExistsException,
)
from app.api.v1.routes.auth.auth_schemas import TokenPayload
from app.api.v1.routes.users.users_repository import search_user_by_user_id
from app.config import settings
from app.database.models.user import User
from app.database.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.OAUTH2_TOKEN_URL)


# Dependency database
def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_token_valid(token: str = Depends(reusable_oauth2)) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise InvalidTokenException

    return token_data


def get_current_user_valid(session: Session = Depends(get_db), token_payload: TokenPayload = Depends(get_token_valid)) -> User:
    user = search_user_by_user_id(session=session, user_id=token_payload.sub)
    if not user:
        raise UserNotExistsException
    if not user.is_active:
        raise InactiveUserException

    return user


def get_current_user_valid_admin(current_user: User = Depends(get_current_user_valid)) -> User:
    if not current_user.is_admin:
        raise UnauthorizedException

    return current_user
