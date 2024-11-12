from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    password: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(default=None)


class UserPublicSchema(BaseModel):
    user_id: int
    username: str
    email: str
    is_admin: bool
    is_active: bool
    date_create_user: datetime
    date_delete_user: datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserPrivateSchema(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    is_admin: bool
    is_active: bool
    date_create_user: datetime
    date_delete_user: datetime | None
    #tokens: List[TokenSchema] = []

    model_config = ConfigDict(from_attributes=True)
