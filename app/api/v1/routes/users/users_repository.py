from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.errors import EmailExistsException, UsernameExistsException
from app.api.security import get_password_hash
from app.api.v1.routes.users.users_schemas import UserCreateSchema, UserUpdateSchema
from app.database.models.user import User


def create_user(session: Session, user: UserCreateSchema, is_admin: bool = False) -> User:
    """
    Añadir un nuevo usuario a la base de datos.

    Args:
        session (Session): Session de base de datos.
        user (User): Nuevo Usuario.
        is_admin (bool): El usuario es tipo admin.

    Returns:
        Usuario creado.
    """

    # Excluye los datos nulls del schema
    user_data = user.model_dump(exclude_unset=True)

    user_data["password"] = get_password_hash(user.password)
    user_data["is_admin"] = is_admin
    user_data["is_active"] = True
    user_data["date_create_user"] = datetime.now()
    user_data["date_delete_user"] = None

    if "email" in user_data:
        user_db = search_user_by_email(session=session, email=user_data["email"])
        if user_db:
            raise EmailExistsException

    if "username" in user_data:
        user_db = search_user_by_username(session=session, username=user_data["username"])
        if user_db:
            raise UsernameExistsException

    user_db = User(**user_data)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


def update_user(session: Session, user: User, new_data_user: UserUpdateSchema) -> User:
    """
    Actualizar datos de usuario.

    Args:
        session (Session): Session de base de datos.
        user (User): Usuario a actualizar.
        new_data_user (UserUpdateSchema): Schema de nuevos datos de usuario.

    Returns:
        Usuario con datos actualizados.
    """

    # Excluye los datos nulls del schema
    user_data = new_data_user.model_dump(exclude_unset=True)

    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        user_data["password"] = hashed_password

    if "email" in user_data:
        user_db = search_user_by_email(session=session, email=user_data["email"])
        if user_db and user_db.user_id != user.user_id:
            raise EmailExistsException

    if "username" in user_data:
        user_db = search_user_by_username(session=session, username=user_data["username"])
        if user_db and user_db.user_id != user.user_id:
            raise UsernameExistsException

    for campo, valor in user_data.items():
        setattr(user, campo, valor)

    # db_user.update(**user_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def search_user_by_email(session: Session, email: str) -> User | None:
    """
    Buscar usuario por email.

    Args:
        session (Session): Session de base de datos.
        email (str): Email a buscar.

    Returns:
        Usuario encontrado.
    """

    statement = select(User).where(User.email == email)
    user = session.execute(statement).scalar_one_or_none()

    return user


def search_user_by_username(session: Session, username: str) -> User | None:
    """
    Buscar usuario por username.

    Args:
        session (Session): Session base de datos.
        username (str): Username a buscar.

    Returns:
        Usuario encontrado.
    """

    statement = select(User).where(User.username == username)
    user = session.execute(statement).scalar_one_or_none()

    return user


def search_user_by_user_id(session: Session, user_id: int) -> User | None:
    """
    Buscar usuario por user id.

    Args:
        session (Session): Session base de datos.
        user_id (str): User id a buscar.

    Returns:
        Usuario encontrado.
    """

    statement = select(User).where(User.user_id == user_id)
    user = session.execute(statement).scalar_one_or_none()

    return user


def search_users(session: Session, skip: int = 0, limit: int = 100) -> Sequence[User] | None:
    """
    Devuelve los usuarios almacenados en la base de datos.

    Args:
        session (Session): Session de base de datos.
        skip (int): Offset de datos.
        limit (int): Numero maximo de usuarios devueltos.

    Returns:
        Lista de usuarios disponibles.
    """

    statement = select(User).offset(skip).limit(limit)
    users = session.execute(statement).scalars().all()

    return users


def delete_user(session: Session, user: User) -> None:
    """
    Eliminar usuario.

    Args:
        session (Session): Session base de datos.
        user (User): Usuario a eliminar.

    Returns:
        None
    """

    session.delete(user)
    session.commit()
