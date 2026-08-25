VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ALEMBIC := $(VENV)/bin/alembic
FASTAPI := $(VENV)/bin/fastapi

.PHONY: help install run dev migrate migration shell

help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make dev         Run FastAPI in development mode"
	@echo "  make migrate     Run database migrations"
	@echo "  make migration   Create new migration"
	@echo "  make shell       Open Python shell"

install:
	$(PIP) install -r requirements.txt

dev:
	$(FASTAPI) dev app/main.py

run:
	$(FASTAPI) run app/main.py

migrate:
	$(ALEMBIC) upgrade head

migration:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

shell:
	$(PYTHON)

dev_compose:
	docker compose -f docker-compose.dev.yml up -d

prod_compose:
	docker compose -f docker-compose.yml up -d