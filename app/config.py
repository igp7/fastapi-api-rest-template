import os
import secrets

from dotenv import load_dotenv

# Load variables de entorno
load_dotenv('./.env')

class DefaultConfig:
    # Project env
    PROJECT_ENV: str = os.getenv("PROJECT_ENV", default="PRO")

    # Estructura de la API
    API_V1_STR: str = "/api/v1"

    # OAuth2
    OAUTH2_TOKEN_URL: str = f"{API_V1_STR}/login"

    # Configuración de la API
    API_TITLE: str = "Template API Rest FastAPI"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = ""
    API_SUMMARY: str = ""
    API_TERMS_OF_SERVICE: str = ""
    API_CONTACT: dict[str:str] = ""
    API_LICENSE_INFO: dict[str:str] = ""
    API_DOCS_URL: str | None ="/docs" # Ruta desde la raiz para acceder a la documentación OpenAPI con Swagger UI
    API_REDOC_URL: str | None = None # None desactiva la documentación con ReDoc
    API_OPENAPI_URL: str = f"{API_V1_STR}/openapi.json"

    # Configuración PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", default="db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", default="5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", default="postgres_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", default="template_api_rest_fastapi")
    POSTGRES_DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Configuración SQLite
    SQLITE_DATABASE_URL: str = "sqlite:///./sql_app.db"

    # Configuración SQLAlchemy
    if PROJECT_ENV == "TEST":
        SQLALCHEMY_DATABASE_URL: str = SQLITE_DATABASE_URL
    elif PROJECT_ENV == "PRO":
        SQLALCHEMY_DATABASE_URL: str = POSTGRES_DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URL: str = None

    # Configuración JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración password hash
    PASSLIB_SCHEMAS = "sha256_crypt"
    PASSLIB_DEPRECATED_SCHEMAS = "auto" # "auto" deja obsoleto todos los schemas que no sean los indicados en "PASSLIB_SCHEMAS"

    # Configuración CORS
    all_cors_origins: list[str] = ["*"]

    # Datos Admin User
    ADMIN_USER_USERNAME: str = os.getenv("ADMIN_USER_USERNAME")
    ADMIN_USER_EMAIL: str = os.getenv("ADMIN_USER_EMAIL")
    ADMIN_USER_PASSWORD: str = os.getenv("ADMIN_USER_PASSWORD")

    # Datos Tests
    TEST_ADMIN_USER_USERNAME: str = "test_admin"
    TEST_ADMIN_USER_EMAIL: str = "test_admin@tests.com"
    TEST_ADMIN_USER_PASSWORD: str = "12345"

    TEST_NORMAL_USER_USERNAME: str = "test_user"
    TEST_NORMAL_USER_EMAIL: str = "test_user@tests.com"
    TEST_NORMAL_USER_PASSWORD: str = "12345"


settings = DefaultConfig()
