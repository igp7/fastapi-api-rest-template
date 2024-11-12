from sqlalchemy.orm import Session

from app.api.v1.routes.users.users_repository import (
    create_user,
    search_user_by_email,
    search_user_by_username,
)
from app.api.v1.routes.users.users_schemas import UserCreateSchema
from app.config import settings
from app.database.base import Base
from app.database.session import engine


def init_db() -> None:
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)


    with Session(engine) as session:
        username_exist = search_user_by_username(session=session, username=settings.ADMIN_USER_USERNAME)
        email_exist = search_user_by_email(session=session, email=settings.ADMIN_USER_EMAIL)
        if not username_exist and not email_exist:
            user_in = UserCreateSchema(
                    username=settings.ADMIN_USER_USERNAME,
                    email=settings.ADMIN_USER_EMAIL,
                    password=settings.ADMIN_USER_PASSWORD)
            user = create_user(session=session, user=user_in, is_admin=True)


def delete_db() -> None:
    # Elimina todas las tablas en la base de datos
    Base.metadata.drop_all(bind=engine)
