# Tail

A backend API for managing tailoring workshops, clients, orders, and measurements.

Tail is designed to simplify the management of tailoring workflows, from registering clients and creating orders to recording measurements and tracking order progress.

## ✨ Features

- User authentication and authorization
- Client management
- Order management
- Order status tracking
- Customer measurements
- Upper and lower body measurements
- Pricing and deposit management
- Delivery date tracking
- RESTful API
- PostgreSQL database
- Async database operations
- Database migrations with Alembic
- Automatic API documentation

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **asyncpg**
- **Alembic**
- **Pydantic**
- **Docker**

## 🏗 Architecture

The project follows a layered architecture:

```text
API
 │
 ▼
Services
 │
 ▼
Repositories
 │
 ▼
SQLAlchemy
 │
 ▼
PostgreSQL
```

This structure keeps API logic, business logic, and database operations separated and makes the project easier to maintain and extend.

## 📦 Domain

The main entities are:

```text
User
 │
 └── Clients
       │
       └── Orders
             │
             └── Measurements
                   ├── Upper
                   └── Lower
```

Measurements are associated with an order so that each order preserves the measurements used for that specific garment.

## 🚀 Getting Started

### Requirements

- Python 3.12+
- PostgreSQL
- Docker (recommended)

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd tail
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

Create your environment file:

```bash
cp .env.example .env
```

Configure your database and application settings inside `.env`.

### Database

Start PostgreSQL with Docker:

```bash
docker compose up -d
```

Run migrations:

```bash
make migrate
```

### Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## 📚 API Documentation

FastAPI provides interactive API documentation:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🗄️ Database Migrations

Create a migration:

```bash
make migration msg="your migration message"
```

Apply migrations:

```bash
make migrate
```

Rollback the latest migration:

```bash
make downgrade
```

## 📁 Project Structure

```text
tail/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── .env.example
└── README.md
```

## 📄 License

This project is private and proprietary.

## 👨‍💻 Author

**Peyman Malek**
