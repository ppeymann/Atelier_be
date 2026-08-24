# Tail Backend

Backend API for **Tail**, a tailoring workshop management system built with **FastAPI** and **PostgreSQL**.

Tail is designed to help tailoring workshops manage clients, orders, measurements, order status, pricing, delivery dates, and other day-to-day operations through a clean and extensible REST API.

---

## ✨ Features

- 🔐 Authentication & authorization
- 👤 User management
- 🧑‍💼 Client management
- 📦 Order management
- 📏 Order-specific body measurements
- 👕 Upper and lower body measurements
- 💰 Order pricing and deposit tracking
- 📅 Delivery date management
- 🔄 Order workflow/status management
- 🗄️ PostgreSQL database
- 🧬 SQLAlchemy 2.0 ORM
- 🔄 Alembic database migrations
- ⚡ Fully asynchronous API
- 🐳 Docker support
- 📝 Automatic OpenAPI documentation
- 🧪 Ready for unit/integration testing
- 🧩 Modular and scalable project structure

---

## 🏗️ Tech Stack

| Technology     | Purpose                 |
| -------------- | ----------------------- |
| Python         | Programming language    |
| FastAPI        | Web framework           |
| SQLAlchemy 2.0 | ORM                     |
| PostgreSQL     | Primary database        |
| asyncpg        | Async PostgreSQL driver |
| Alembic        | Database migrations     |
| Pydantic v2    | Data validation         |
| Docker         | Containerization        |
| Uvicorn        | ASGI server             |

---

## 📁 Project Structure

```text
tail/
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   └── routes/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── ...
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── ...
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── order.py
│   │   ├── measurement.py
│   │   └── ...
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── order.py
│   │   └── measurement.py
│   │
│   ├── repositories/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── order.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── order.py
│   │   └── ...
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

---

# 🧠 Architecture

Tail follows a layered architecture to keep business logic, database access, and HTTP concerns separated.

```text
HTTP Request
     │
     ▼
  Router
     │
     ▼
  Service
     │
     ▼
 Repository
     │
     ▼
 SQLAlchemy
     │
     ▼
 PostgreSQL
```

### Router

Responsible for:

- HTTP endpoints
- Request/response handling
- Dependency injection
- Authentication dependencies
- HTTP status codes

Routers should avoid containing complex business logic.

### Service

Responsible for:

- Business rules
- Application logic
- Coordinating repositories
- Validating domain-specific operations

### Repository

Responsible for:

- Database queries
- Creating records
- Updating records
- Deleting records
- Loading relationships

### Models

SQLAlchemy database models representing the application's persistent data.

### Schemas

Pydantic models used for:

- Request validation
- Response serialization
- API contracts

---

# 🗃️ Data Model

The main domain entities are:

```text
User
 │
 └── Clients
       │
       └── Orders
             │
             └── OrderMeasurement
                    ├── UpperMeasurement
                    └── LowerMeasurement
```

## User

Represents an authenticated application user.

```text
User
 └── Client[]
```

A user can manage multiple clients.

---

## Client

Represents a customer of the tailoring workshop.

```text
Client
 └── Order[]
```

A client can have multiple orders.

---

## Order

Represents a tailoring order.

An order contains information such as:

- Client
- Clothing type
- Fabric type
- Fabric color
- Lining
- Price
- Deposit
- Delivery date
- Order status
- Notes

---

## Measurements

Measurements belong to an **order**, rather than directly to a client.

This is intentional.

A client's measurements can change over time, but an order should preserve the exact measurements used to produce that garment.

```text
Order
  │
  └── OrderMeasurement
        ├── UpperMeasurement
        │     ├── Chest
        │     ├── Shoulder
        │     ├── Sleeve
        │     └── ...
        │
        └── LowerMeasurement
              ├── Waist
              ├── Hip
              ├── Thigh
              └── ...
```

---

# 🔄 Order Status

Orders follow a simple production workflow:

```text
RECEIVED
   │
   ▼
CUTTING
   │
   ▼
SEWING
   │
   ▼
FINISHING
   │
   ▼
READY
```

The status is represented using a Python `StrEnum` and PostgreSQL enum type.

Example:

```python
class Status(StrEnum):
    received = "RECEIVED"
    cutting = "CUTTING"
    sewing = "SEWING"
    finishing = "FINISHING"
    ready = "READY"
```

---

# ⚙️ Requirements

Before running the project, make sure you have:

- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose (recommended)
- Git

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone <repository-url>
cd tail
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

If using `pyproject.toml`:

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tail

SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

ENVIRONMENT=development
DEBUG=true
```

Never commit `.env` to Git.

Use `.env.example` as a template:

```env
DATABASE_URL=

SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=

ENVIRONMENT=development
DEBUG=true
```

---

# 🐘 PostgreSQL

If you're using Docker:

```bash
docker compose up -d db
```

Check running containers:

```bash
docker compose ps
```

Stop the database:

```bash
docker compose down
```

---

# 🗄️ Database Migrations

Tail uses **Alembic** for database schema migrations.

## Create a migration

The project provides a Makefile command:

```bash
make migration msg="Add orders table"
```

This runs:

```bash
alembic revision --autogenerate -m "Add orders table"
```

---

## Apply migrations

```bash
make migrate
```

Equivalent to:

```bash
alembic upgrade head
```

---

## Roll back the latest migration

```bash
make downgrade
```

Equivalent to:

```bash
alembic downgrade -1
```

---

## Check migration status

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

---

# ▶️ Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

Or if a Makefile command exists:

```bash
make run
```

The API will be available at:

```text
http://localhost:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

### OpenAPI Schema

```text
http://localhost:8000/openapi.json
```

---

# 🔌 API Overview

The API is organized around the following resources.

## Authentication

```text
POST /auth/register
POST /auth/login
POST /auth/refresh
GET  /auth/me
```

---

## Clients

```text
GET    /clients
GET    /clients/{client_id}
POST   /clients
PATCH  /clients/{client_id}
DELETE /clients/{client_id}
```

---

## Orders

```text
GET    /orders
GET    /orders/{order_id}
POST   /orders
PATCH  /orders/{order_id}
DELETE /orders/{order_id}
```

---

## Measurements

Measurements are associated with an order.

```text
GET   /orders/{order_id}/measurements
POST  /orders/{order_id}/measurements
PATCH /orders/{order_id}/measurements
```

The exact endpoints may evolve as the API grows.

---

# 📦 Example Order

```json
{
  "client_id": "7b8e9a4d-3f2a-4d1f-9f3a-8d2f8b3a12ab",
  "clothing_type": "Suit",
  "fabric_type": "Wool",
  "fabric_color": "Black",
  "lining": "Silk",
  "price": 15000000,
  "deposit": 5000000,
  "delivery": "2026-09-15",
  "status": "RECEIVED"
}
```

---

# 📏 Example Measurements

```json
{
  "upper": {
    "chest": 102,
    "shoulder": 45,
    "sleeve": 62
  },
  "lower": {
    "waist": 84,
    "hip": 98,
    "thigh": 58
  }
}
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run only unit tests:

```bash
pytest tests/unit
```

Run integration tests:

```bash
pytest tests/integration
```

---

# 🧹 Code Quality

Recommended development tools:

```bash
ruff check .
```

Format code:

```bash
ruff format .
```

Type checking:

```bash
mypy app
```

---

# 🐳 Docker

Build the application:

```bash
docker compose build
```

Start all services:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f
```

Stop services:

```bash
docker compose down
```

---

# 🔒 Security

The application should follow these principles:

- Passwords must never be stored in plain text.
- Authentication tokens must be securely signed.
- Secrets must be provided through environment variables.
- `.env` must never be committed.
- Database credentials must not be hardcoded.
- Protected endpoints must require authentication.
- User-owned resources must be authorized before access.

---

# 📐 Design Principles

Tail follows several core principles:

### Separation of concerns

HTTP, business logic, and database access remain separated.

### Async-first

Database and HTTP operations use asynchronous APIs where appropriate.

### Type safety

Python type hints, Pydantic, and SQLAlchemy 2.0 typed mappings are used throughout the project.

### Database integrity

Relationships, foreign keys, constraints, and enums are enforced at the database level whenever possible.

### Order snapshots

Order-specific information, especially measurements, should remain attached to the order so historical orders remain accurate.

---

# 🛠️ Makefile

Common commands:

```bash
make run
make migration msg="your migration message"
make migrate
make downgrade
```

Example:

```bash
make migration msg="Add order measurements"
make migrate
```

---

# 🌱 Development Workflow

A typical development workflow is:

```text
1. Create/modify SQLAlchemy models
              │
              ▼
2. Generate Alembic migration
              │
              ▼
3. Review migration
              │
              ▼
4. Apply migration
              │
              ▼
5. Implement repository
              │
              ▼
6. Implement service
              │
              ▼
7. Implement API endpoint
              │
              ▼
8. Add tests
```

Example:

```bash
make migration msg="Add order measurements"
make migrate

uvicorn app.main:app --reload
```

---

# 🤝 Contributing

1. Create a new branch:

```bash
git checkout -b feature/order-measurements
```

2. Make your changes.

3. Run tests:

```bash
pytest
```

4. Run linting:

```bash
ruff check .
```

5. Create and review migrations if database models changed:

```bash
make migration msg="Describe your change"
make migrate
```

6. Commit your changes:

```bash
git add .
git commit -m "feat: add order measurements"
```

7. Push your branch:

```bash
git push origin feature/order-measurements
```

---

# 🗺️ Roadmap

- [x] User management
- [x] Client management
- [x] Order management
- [x] Order status workflow
- [x] Order measurements
- [x] Upper/lower measurements
- [ ] Authentication improvements
- [ ] Refresh token support
- [ ] Google OAuth
- [ ] Order history
- [ ] Measurement history
- [ ] Notifications
- [ ] Dashboard statistics
- [ ] File/image attachments
- [ ] Automated tests
- [ ] Production Docker setup
- [ ] CI/CD
- [ ] Monitoring and logging

---

# 📄 License

This project is currently private and proprietary.

All rights reserved.

---

## 👨‍💻 Author

**Peyman Malek**

Tail — Tailoring Workshop Management System
