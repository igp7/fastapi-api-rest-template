from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_error_handlers
from app.api.v1.main import api_router
from app.config import settings
#from app.database.database_repository import init_db

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    summary=settings.API_SUMMARY,
    version=settings.API_VERSION,
    terms_of_service=settings.API_TERMS_OF_SERVICE,
    contact=settings.API_CONTACT,
    license_info=settings.API_LICENSE_INFO,
    docs_url=settings.API_DOCS_URL,
    redoc_url=settings.API_REDOC_URL
)

# registro de errores
register_error_handlers(app)

# Configuracion de CORS
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# init_db()
