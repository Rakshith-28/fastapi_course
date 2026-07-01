# FastAPI Course Project

A social-media–style REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.
Users can register, log in (JWT auth), create posts, and vote on posts.

🌐 **Live demo:** https://fastapi-course-1-mqho.onrender.com/docs

[![Build and Test](https://github.com/Rakshith-28/fastapi_course/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/Rakshith-28/fastapi_course/actions/workflows/build-and-test.yml)

---

## Features

- 🔐 **JWT authentication** with hashed passwords (bcrypt/passlib)
- 📝 **Posts CRUD** — create, read, update, delete (owner-only for update/delete)
- 👍 **Voting** — one vote per user per post
- 👤 **Users** — registration and lookup
- 🗄️ **PostgreSQL** via SQLAlchemy ORM
- 🔀 **Alembic** database migrations
- ⚙️ **Environment-based config** (pydantic-settings)
- ✅ **34 automated tests** (pytest) against an isolated test database
- 🐳 **Docker** + docker-compose for local development
- 🔄 **CI** via GitHub Actions (tests + Docker build on every push)

---

## Tech stack

| Layer | Tech |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | OAuth2 password flow + JWT (python-jose) |
| Validation/Settings | Pydantic v2 / pydantic-settings |
| Tests | pytest |
| Containers | Docker / docker-compose |
| CI | GitHub Actions |

---

## Project structure

```
app/
  main.py            # FastAPI app + router registration
  config.py          # Settings loaded from environment
  database.py        # SQLAlchemy engine/session
  models.py          # ORM models (User, Post, Vote)
  schemas.py         # Pydantic request/response schemas
  oauth2.py          # JWT creation/verification
  utils.py           # Password hashing helpers
  routers/
    auth.py          # /login
    user.py          # /users
    post.py          # /posts
    vote.py          # /vote
alembic/             # Migrations
tests/               # pytest suite
Dockerfile
docker-compose.yml
.github/workflows/   # CI
```

---

## Environment variables

The app reads config from environment variables (or a local `.env` file). Required keys:

| Key | Example |
|---|---|
| `DATABASE_HOSTNAME` | `localhost` |
| `DATABASE_PORT` | `5432` |
| `DATABASE_NAME` | `fastapi` |
| `DATABASE_USERNAME` | `postgres` |
| `DATABASE_PASSWORD` | `postgres123` |
| `SECRET_KEY` | *(long random hex string)* |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

> `.env` is git-ignored — never commit real secrets.
> Generate a secret key with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## Running locally (without Docker)

**Prerequisites:** Python 3.12, PostgreSQL running locally, a database created (e.g. `fastapi`).

```bash
# 1. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with the variables listed above

# 4. Apply migrations (or let create_all build tables on startup)
alembic upgrade head

# 5. Run the server
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## Running with Docker

Spins up the API and a Postgres database together:

```bash
docker-compose up --build
```

The API is available at **http://localhost:8000/docs**. Postgres data persists in a named volume.

---

## Running the tests

Tests use a **separate database** named `<DATABASE_NAME>_test` (e.g. `fastapi_test`). Create it once:

```bash
createdb fastapi_test           # or via pgAdmin / psql
```

Then run:

```bash
pytest -v
```

The suite recreates the schema for each test, so tests are fully isolated and never touch your dev data.

---

## Database migrations (Alembic)

Whenever you change a model:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

---

## API endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | – | Health/welcome message |
| `POST` | `/users/` | – | Register a new user |
| `GET` | `/users/{id}` | – | Get a user by id |
| `POST` | `/login` | – | Log in (form data: `username`, `password`) → JWT |
| `GET` | `/posts/` | ✅ | List posts (with vote counts); supports `limit`, `skip`, `search` |
| `POST` | `/posts/` | ✅ | Create a post |
| `GET` | `/posts/{id}` | ✅ | Get one post (with vote count) |
| `PUT` | `/posts/{id}` | ✅ (owner) | Update a post |
| `DELETE` | `/posts/{id}` | ✅ (owner) | Delete a post |
| `POST` | `/vote/` | ✅ | Vote (`dir: 1`) or un-vote (`dir: 0`) on a post |

**Auth:** send `Authorization: Bearer <access_token>` (obtained from `/login`).

---

## Deployment

Deployed on [Render](https://render.com) (free tier) with a managed PostgreSQL instance.
Environment variables are configured in the Render dashboard; every push to `main` triggers an automatic redeploy.

> Note: the free tier sleeps after ~15 min of inactivity — the first request after that takes ~30–50s to wake.
