# Template API REST FastAPI 
Template de un servicio API Rest desarrollado en Python con el framework FastAPI, Pydantic, SQLAlchemy, PostgreSQL,
Pytest y Docker. El template cubre la de gestión de usuarios y usa tokens jwt para autenticación.


## Indice
- [Tecnología](#tecnología)
- [Requisitos](#requisitos)
- [Configuración](#configuracion)
  - [Variables de entorno](#variables-de-entorno)
- [Instalar dependencias](#instalar-dependencias)
- [Documentación (OpenAPI)](#documentacion-OpenAPI)
- [Comandos Makefile](#comandos-makefile)
  - [Comandos ejecución entorno PRO](#comandos-ejecucion-entorno-pro)
  - [Comandos ejecución entorno DEV](#comandos-ejecucion-entorno-dev)
  - [Comandos ejecución tests](#comandos-ejecucion-tests)
- [Endpoints](#endpoints)
  - [Users](#users)
  - [Auth](#auth)
- [CI-CD](#ci-cd)
   - [CI (Continuous Integration)](#ci-continuous-integration)
- [Ejemplo de expansion de este template](#ejemplo-de-expansion-de-este-template)


## Tecnología
- **Web Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Autenticación:** PyJWT (JSON Web Token)
- **Serialización, Deserialización y Validación:** Pydantic
- **Documentación:** Swagger-UI
- **Authentication:** PyJWT
- **Tests:** Pytest
- **Cobertura de código:** Pytest-cov
- **Base De Datos:** PostgreSQL y SQLite
- **Gestor de dependencias/environments:** UV
- **Linter/Formatter:** Ruff
- **Contenirizacion:** Docker y docker-compose
- **CI/CD:** Github Actions


## Requisitos
- [UV](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/get-started)
- [Docker-Compose](https://docs.docker.com/compose/install/)
- [Python 3.12](https://www.python.org/downloads/)
- [Github](https://github.com)
- [Makefile](https://www.gnu.org/software/make/)


## Configuración
### Variables de entorno
````
# Las opciones de PROJECT_ENV son PRO y TEST
PROJECT_ENV

# Datos del primer usuario con rol admin
ADMIN_USER_USERNAME
ADMIN_USER_EMAIL
ADMIN_USER_PASSWORD

# Datos de configuracion de POSTGRES
POSTGRES_SERVER # Host desde el equipo local
POSTGRES_PORT
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

# Secret key para JWT
JWT_SECRET_KEY
````

## Instalar dependencias
```sh
make install-dependencias
```
o
```sh
uv sync --all-extras --dev
source .venv/bin/activate
```


## Documentación (OpenAPI)
La visualización de la documentación de OpenAPI por defecto es en **localhost:8000/docs**.


## Comandos Makefile
### Comandos ejecución entorno PRO
- Levantar el entorno pro.
    ```sh
    make pro-up
    ```
  
- Suspender el entorno pro.
    ```sh
    make pro-down
    ```
  
- Suspender el entorno pro y eliminar los volumenes docker.
    ```sh
    make pro-down-remove-data
    ```
  
- Suspender el entorno pro y eliminar los volumenes e imagenes de docker.
    ```sh
    make pro-down-remove-all
    ```

- Visualizar los logs del entorno pro.
    ```sh
    make pro-logs
    ```

### Comandos ejecución entorno DEV
- Levantar el entorno dev.
    ```sh
    make dev-up
    ```
  
- Suspender el entorno dev.
    ```sh
    make dev-down
    ```
  
- Suspender el entorno dev y eliminar los volumenes docker.
    ```sh
    make dev-down-remove-data
    ```
  
- Suspender el entorno dev y eliminar los volumenes e imagenes de docker.
    ```sh
    make dev-down-remove-all
    ```

- Visualizar los logs del entorno dev.
    ```sh
    make dev-logs
    ```

### Comandos ejecución tests
- Ejecutar tests sin coverage:
   ```sh
   make tests
   ```

- Ejecutar tests repository sin coverage:
   ```sh
   make tests-repository
   ```
  
- Ejecutar tests api sin coverage:
   ```sh
   make tests-api
   ```
     
- Ejecutar tests con coverage sin reporte en html:
   ```sh
   make tests-cov
   ```
     
- Ejecutar tests con coverage con reporte en html:
   ```sh
   make tests-cov-html
   ```

**NOTA:** La API Rest usa por defecto el host *localhost* y el puerto *8000*.


## Endpoints
Roles: user, admin

### Users
| Endpoint            | HTTP Method | Result              | Role  |
|:--------------------|:---:|---------------------|-------|
| `/users`            | `POST`  | Crear nuevo usuario | user, admin |
| `/users`            | `GET`  | Obtener todos los usuarios | admin |
| `/users/{username}` | `GET`  | Obtener un usuario por username | admin |
| `/users/{username}` | `PUT`  | Actualizar un usuario por username | admin |
| `/users/{username}` | `DELETE`  | Eliminar un usuario por username | admin |
| `/users/me`         | `GET`  | Obtener el usuario actual | user, admin |
| `/users/me`         | `PUT`  | Actualizar el usuario actual | user, admin |
| `/users/me`         | `DELETE`  | Eliminar el usuario actual | user, admin |

> La implementación de los endpoints de user esta en  [app/api/v1/routers/users/users_routers.py](app/api/v1/routes/users/users_routes.py).

### Auth
| Endpoint | HTTP Method | Result | Role |
|:---|:---:|---|---|
| `/auth/login`  | `POST`  | Login de un usuario  | user, admin |

> La implementación de los endpoints de auth esta en [app/api/v1/routers/auth/auth_routers.py](app/api/v1/routes/auth/auth_routes.py).


## CI-CD
### CI (Continuous Integration)
El workflow de CI (ci.yml) utiliza Github Actions, como el Github Action [setup-uv](https://github.com/astral-sh/setup-uv) para utilizar comandos de uv, más información [aquí](https://docs.astral.sh/uv/guides/integration/github/).
El workflow ejecuta los tests de API y los test de repositoris cuando se realiza un pull-request a main y develop o un push a develop.


## Ejemplo de expansion de este template
Necesitas añadir *items* que permita a los usuarios hacer CRUD en sus artículos:
1. Crear un modelo de base de datos `item` en [app/database/models](./app/database/models).
2. Crear un directorio `item` en el directorio [app/api/v1/routers](./app/api/v1/routes)
   1. Crear schemas de `item` para load, dump y validación en [app/api/v1/routers/item/item_schemas.py](app/api/v1/routes/item/item_schemas.py).
   2. Crear funciones repository de `item` en [app/api/v1/routers/item/item_repository.py](app/api/v1/routes/item/item_repository.py).
   3. Crear funciones endpoint de `item` en [app/api/v1/routers/item/item_routers.py](app/api/v1/routes/item/item_routers.py).
3. Añadir el APIRouter de `items` en [app/api/v1/main.py](./app/api/v1/main.py) 
4. Crea nuevos tests para el nuevo módulo:
   1. Crear el directorio de tests de api en el directorio [tests/api/routes](./tests/api/routes) (convención para este proyecto) y crear ficheros por cada función a testear para escribir los tests.
   2. Crear el directorio de tests de repository en el directorio [tests/repository](./tests/repository) (convención para este proyecto) y crear ficheros por cada función a testear para escribir los tests.
   3. Crear fichero de funciones utiles para `item` en el directorio [tests/utils](./tests/utils) (convención para este proyecto).
   4. Crear peticiones en postman (Opcional).
5. Añadir los endpoints en [README](#endpoints)


## Aviso de descargo de responsabilidad
En ningún caso me hago responsable por daños y perjuicios, incluidos, entre otros, daños y perjuicios indirectos o de carácter secundario, o daños y perjuicios por pérdidas o beneficios derivados de, o relacionados con, la utilización de este software.

Tú, como usuario, actúas por tu cuenta y riesgo si decides utilizar este software.


## Contribución
Siéntete libre de realizar cualquier sugerencia o mejora al proyecto.
