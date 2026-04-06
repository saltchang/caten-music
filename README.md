# [Caten Music](https://music.caten-church.org)

A music data management system for **[Caten Church](https://caten-church.org)**.

- View and search the songs you need.
- Sign up to create a song list and share it with your partner.
- Become an admin and create a new song, or edit an old one.

Also see **[Church Music API](https://github.com/saltchang/church-music-api)**

## Tech Stack

- [Python 3.14](https://www.python.org)
- [FastAPI](https://fastapi.tiangolo.com) + [uvicorn](https://www.uvicorn.org)
- [PostgreSQL](https://www.postgresql.org) + [SQLAlchemy 2.0](https://www.sqlalchemy.org) (async)
- [Docker](https://www.docker.com)
- [uv](https://docs.astral.sh/uv/) (package manager)

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com) and Docker Compose
- Or [uv](https://docs.astral.sh/uv/) for local development without Docker

### Setup

Create a local `.env` file from the example:

```bash
cp env.example .env
```

Edit `.env` and fill in the required values (`SECRET_KEY`, `HASH_SALT`, `CHURCH_MUSIC_API_URL`). See [Environment Variables](docs/ENVIRONMENT_VARIABLES.md) for details.

### Run with Docker

```bash
docker compose build
docker compose up -d
```

The API will be available at [http://localhost:3777](http://localhost:3777).

Check logs:

```bash
docker compose logs -f
```

### Run Locally (without Docker)

```bash
uv sync            # Install dependencies
make dev            # Dev server on http://localhost:3777
```

Requires a running PostgreSQL instance (configure `DATABASE_URL` in `.env`).

### Verify

```bash
curl http://localhost:3777/api/health
# {"status":"OK"}
```

## Development

```bash
uv sync --group dev         # Install dev dependencies

make test                   # Run all tests
make lint                   # Lint
make format                 # Format
make typecheck              # Type check
make check                  # All of the above
```

See [Commands](docs/COMMANDS.md) for the full list.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Clean Architecture layers and design decisions
- [Commands](docs/COMMANDS.md) - All development commands
- [Environment Variables](docs/ENVIRONMENT_VARIABLES.md) - Configuration reference
