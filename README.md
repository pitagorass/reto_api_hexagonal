# Reto AWS - API (Hexagonal Architecture) - Skeleton

## Overview
This project is a minimal Python API implementing **hexagonal architecture** (ports & adapters) for the Reto AWS.
It includes two endpoints required by HU1/HU7: `POST /guardarpersona` and `GET /consultarpersona/{id}`.

The app reads configuration (DB host, user, password, etc.) from environment variables so it can be injected
by **SSM Parameter Store / Secrets Manager** when deployed to ECS (as required by HU5).

## Structure
- `app/` - application code
  - `main.py` - FastAPI entrypoint (adapter: web)
  - `models.py` - Pydantic models
  - `ports/repository.py` - repository interface (port)
  - `adapters/db/postgres.py` - Postgres adapter (implements the repository port)
  - `services/person_service.py` - domain/application service (use case)
- `Dockerfile` - to build container image
- `requirements.txt`
- `docker-compose.yml` - optional for local testing with a local Postgres
- `scripts/init_db.sql` - helper SQL to create schema/table
- `tests/` - pytest basics

## Environment variables (injected by ECS SSM/Secrets)
- `DB_HOST` (required)
- `DB_PORT` (default: 5432)
- `DB_NAME` (default: appdb)
- `DB_USER` (required)
- `DB_PASS` (required)
- `API_PORT` (default: 3000)

## Local quickstart (with docker-compose)
1. Copy `.env.example` → `.env` and fill values for DB_*.
2. `docker-compose up --build`
3. Visit `http://localhost:3000/health`

## Usage in AWS ECS (notes)
- Put non-sensitive config into SSM Parameter Store and secrets (DB_PASS) into Secrets Manager.
- In the ECS Task Definition, use `secrets` to inject SSM/Secrets Manager ARNs into container env variables.
- The code reads environment variables via `os.environ` and uses them to connect to RDS.

## License
MIT
