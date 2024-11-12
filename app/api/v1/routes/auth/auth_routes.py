from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import security
from app.api.dependencies import get_db
from app.api.errors import (
    InactiveUserException,
    LoginErrorException,
    PasswordErrorException,
    UserNotExistsException,
)
from app.api.v1.routes.auth.auth_repository import authenticate
from app.api.v1.routes.auth.auth_schemas import TokenSchema

auth_router = APIRouter()


@auth_router.post("/login")
def login_access_token(
        session: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
) -> TokenSchema:
    """
    Autenticación de usuario y obtención de access token.
    """

    try:
        user = authenticate(session=session, username=form_data.username, password=form_data.password)
    except (UserNotExistsException, PasswordErrorException):
        raise LoginErrorException


    if not user.is_active:
        raise InactiveUserException

    access_token = security.create_access_token(user.user_id)

    return TokenSchema(access_token=access_token)
