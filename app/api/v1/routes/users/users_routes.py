from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.commun_schemas import MessageSchema
from app.api.dependencies import (
    get_current_user_valid,
    get_current_user_valid_admin,
    get_db,
)
from app.api.errors import (
    UserExistsException,
    UserNotExistsException,
)
from app.api.v1.routes.users.users_repository import (
    create_user,
    delete_user,
    search_user_by_username,
    search_users,
    update_user,
)
from app.api.v1.routes.users.users_schemas import (
    UserCreateSchema,
    UserPrivateSchema,
    UserPublicSchema,
    UserUpdateSchema,
)
from app.database.models.user import User

users_router = APIRouter()


@users_router.get("/users/me",
                  response_model=UserPrivateSchema,
                  status_code=200)
def get_user_me(*,
           current_user: User = Depends(get_current_user_valid)
) -> Any:
    """
    Get current user.
    """

    if not current_user:
        raise UserNotExistsException

    return current_user


@users_router.put("/users/me",
                  response_model=UserPrivateSchema,
                  status_code=200)
def update_user_me(*,
                   session: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user_valid),
                   user_in: UserUpdateSchema
) -> Any:
    """
    Update own user.
    """

    if not current_user:
        raise UserNotExistsException

    new_user = update_user(session, current_user, user_in)

    return new_user


@users_router.delete("/users/me",
                     response_model=MessageSchema,
                     status_code=200)
def delete_user_me(*,
                   session: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user_valid)
) -> Any:
    """
    Delete own user.
    """

    if not current_user:
        raise UserNotExistsException

    delete_user(session=session, user=current_user)

    return MessageSchema(message=f"The user with username {current_user.username} delete in the system.")


@users_router.post("/users",
                   response_model=UserPublicSchema,
                   status_code=201)
def create_new_user(*,
                    session: Session = Depends(get_db),
                    user_data: UserCreateSchema
) -> Any:
    """
    Create new user.
    """

    user = search_user_by_username(session=session, username=user_data.username)
    if user:
        raise UserExistsException

    user = create_user(session=session, user=user_data)

    return user


@users_router.get("/users",
                  dependencies=[Depends(get_current_user_valid_admin)],
                  response_model=list[UserPrivateSchema],
                  status_code=200)
def get_users(*,
                  session: Session = Depends(get_db),
                  skip: Annotated[
                      int | None,
                      Query(
                          title="Offset query",
                          description="",
                          ge=0,
                      ),
                  ] = None,
                  limit: Annotated[
                      int | None,
                      Query(
                          title="Limit of users",
                          description="",
                          ge=0,
                      ),
                  ] = None
) -> Any:
    """
    Get all users.
    """

    users = search_users(session=session, skip=skip, limit=limit)

    return users


@users_router.get("/users/{username}",
                  dependencies=[Depends(get_current_user_valid_admin)],
                  response_model=UserPrivateSchema,
                  status_code=200)
def get_user_by_username(*,
             session: Session = Depends(get_db),
             username: str
) -> Any:
    """
    Get a specific user by username.
    """

    user = search_user_by_username(session=session, username=username)
    if not user:
        raise UserNotExistsException

    return user


@users_router.put("/users/{username}",
                  dependencies=[Depends(get_current_user_valid_admin)],
                  response_model=UserPrivateSchema,
                  status_code=200)
def update_user_by_username(*,
                session: Session = Depends(get_db),
                username: str,
                user_in: UserUpdateSchema
) -> Any:
    """
    Update a user.
    """

    user = search_user_by_username(session=session, username=username)
    if not user:
        raise UserNotExistsException

    new_user = update_user(session, user, user_in)

    return new_user


@users_router.delete("/users/{username}",
                     dependencies=[Depends(get_current_user_valid_admin)],
                     response_model=MessageSchema,
                     status_code=200)
def delete_user_by_username(*,
                 session: Session = Depends(get_db),
                 username: str
) -> Any:
    """
    Delete a user.
    """

    user = search_user_by_username(session=session, username=username)
    if not user:
        raise UserNotExistsException

    delete_user(session=session, user=user)

    return MessageSchema(message=f"The user with username {username} delete in the system.")
