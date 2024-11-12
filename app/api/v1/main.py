from fastapi import APIRouter

from app.api.v1.routes.auth.auth_routes import auth_router
from app.api.v1.routes.users.users_routes import users_router

api_router = APIRouter()

api_router.include_router(users_router, tags=["users"])
api_router.include_router(auth_router, tags=["auth"])
