from pydantic import BaseModel

"""
class TokenBaseSchema(BaseModel):
    token_id: int
    jti: str
    token_type: str
    user_identity: str
    expires: datetime

    model_config = ConfigDict(from_attributes=True)
"""


# Contenido de JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


# Access token response
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
