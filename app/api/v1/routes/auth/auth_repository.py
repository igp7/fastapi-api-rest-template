from sqlalchemy.orm import Session

from app.api.errors import PasswordErrorException, UserNotExistsException
from app.api.security import verify_password
from app.api.v1.routes.users.users_repository import search_user_by_username
from app.database.models.user import User


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    """
    Valida las credenciales de usuario.

    Args:
        session (Session): Session de database.
        username (str): username user.
        password (str): password user.

    Returns:
        User | None -> Retorna el usuario autenticado.
    """

    db_user = search_user_by_username(session=session, username=username)

    if not db_user:
        raise UserNotExistsException
    if not verify_password(password, db_user.password):
        raise PasswordErrorException

    return db_user
