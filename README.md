# Ez Shop Backend

A Django REST Framework backend for a multi-role e-commerce platform with JWT authentication, role-based access control, and Docker support.

## Tech Stack

- **Python** 3.12
- **Django** 6.0 + Django REST Framework
- **PostgreSQL** 16
- **JWT** via `djangorestframework-simplejwt`
- **API Docs** via `drf-spectacular` (Swagger / ReDoc)
- **Package Manager** — [uv](https://github.com/astral-sh/uv)
- **Containerization** — Docker + Docker Compose

---

## Project Structure

```
ez-shop-backend/
├── apps/
│   ├── users/        # Auth, roles, profile management
│   └── products/     # Product & category management
├── common/           # Shared mixins, permissions, base services
├── config/           # Django settings, URLs, WSGI/ASGI
├── Dockerfile
├── docker-compose.yaml        # Production
├── docker-compose.local.yaml  # Local dev (with volume mount)
└── pyproject.toml
```

---

## User Roles

| Role       | Capabilities                                      |
|------------|---------------------------------------------------|
| Public     | Browse & view active products                     |
| Merchant   | All public access + create & manage own products  |
| Admin      | Full access to all users, merchants, and products |

---

## API Endpoints

### Auth — `/api/v1/auth/`

| Method | Endpoint                              | Access   | Description              |
|--------|---------------------------------------|----------|--------------------------|
| POST   | `register/`                           | Public   | Register a new user      |
| POST   | `login/`                              | Public   | Login and get JWT tokens |
| GET/PUT| `profile/`                            | Auth     | View / update profile    |
| POST   | `change-password/`                    | Auth     | Change password          |
| GET    | `admin/users/`                        | Admin    | List all users           |
| GET    | `admin/merchants/`                    | Admin    | List all merchants       |
| POST   | `admin/users/<id>/deactivate/`        | Admin    | Deactivate a user        |

### Products — `/api/v1/products/`

| Method | Endpoint                  | Access   | Description              |
|--------|---------------------------|----------|--------------------------|
| GET    | `products/`               | Public   | List active products     |
| GET    | `products/<id>/`          | Public   | Get product detail       |
| POST   | `products/create/`        | Merchant | Create a product         |

Supports filtering by `category`, search by `name`/`description`, and ordering by `price`/`created_at`.

### API Docs

| URL           | Description        |
|---------------|--------------------|
| `/api/docs/`  | Swagger UI         |
| `/api/redoc/` | ReDoc              |
| `/api/schema/`| OpenAPI schema     |

---

## Getting Started

### Prerequisites

- Docker & Docker Compose

### 1. Clone the repo

```bash
git clone <repo-url>
cd ez-shop-backend
```

### 2. Configure environment

Copy `.env.local` and fill in your values:

```bash
cp .env.local .env.local
```

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES_USER=postgres_ez_shop
POSTGRES_PASSWORD=your-password
POSTGRES_DB=ez_shop_db
POSTGRES_PORT=5432
POSTGRES_HOST=db

ACCESS_TOKEN_LIFETIME_MINUTES=120
REFRESH_TOKEN_LIFETIME_DAYS=1
```

### 3. Run with Docker

**Local dev** (with live code reload via volume mount):

```bash
docker compose -f docker-compose.local.yaml up --build
```

**Production:**

```bash
docker compose up --build
```

The app will be available at `http://localhost:8007`.

---

## Local Development (without Docker)

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) installed
- PostgreSQL running locally

### Setup

```bash
uv sync
cp .env.local .env.local   # update POSTGRES_HOST to localhost

uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

---

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain tokens via `POST /api/v1/auth/login/`.
