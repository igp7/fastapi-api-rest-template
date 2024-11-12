# Instalar dependencias
install-dependencias:
	uv sync --all-extras --dev
	source .venv/bin/activate


# Ejecución entorno PRO
pro-up:
	docker compose -f docker-compose.yml up -d

pro-down:
	docker compose -f docker-compose.yml down

pro-down-remove-data:
	docker compose -f docker-compose.yml down -v

pro-down-remove-all:
	docker compose -f docker-compose.yml down -v --rmi all

pro-logs:
	docker compose -f docker-compose.yml logs --follow


# Ejecución entorno DEV
dev-up:
	docker compose -f docker-compose.yml up -d
	echo "Comienza la cuenta atrás..."
	sleep 60
	echo "60 segundos han pasado"
	docker compose -f docker-compose.yml stop api
	uv run fastapi dev app/main.py

dev-down:
	docker compose -f docker-compose.yml down

dev-down-remove-data:
	docker compose -f docker-compose.yml down -v

dev-down-remove-all:
	docker compose -f docker-compose.yml down -v --rmi all

dev-logs:
	docker compose -f docker-compose.yml logs --follow


# Ejecución de Tests
test:
	uv run pytest tests/

test-api:
	uv run pytest tests/api/

test-repository:
	uv run pytest tests/repository/

test-cov:
	uv run pytest --cov=app/ tests/*

test-cov-html:
	uv run pytest --cov=app/ tests/* --cov-report=html