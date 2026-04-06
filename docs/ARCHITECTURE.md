# Architecture

This is a **FastAPI application** following Clean Architecture (Robert C. Martin). The backend lives in `app/` and serves a JSON API for a React frontend (pending).

## Clean Architecture Layers

Dependencies flow inward: **API → Service → Core ← Repository/Infrastructure**

### Core Layer (`app/core/`)

The innermost layer. Zero external dependencies — pure Python only.

- **Entities** (`core/entities/`) — Plain `@dataclass` domain objects: `User`, `UserProfile`, `SongList`, `InvitationCode`, `SongReport`, `MusicWork`, `MusicVersion`. These are NOT ORM models.
- **Interfaces** (`core/interfaces/`) — `Protocol` contracts for repositories (`UserRepository`, `SonglistRepository`, `SongRepository`, etc.) and infrastructure (`PasswordHasher`, `TokenService`, `MailService`, `FileService`). The service layer codes against these, never concrete implementations.
- **Exceptions** (`core/exceptions.py`) — Domain-specific errors (`InvalidCredentialsError`, `SonglistNotFoundError`, etc.), mapped to HTTP codes in the API layer.
- **Validators** (`core/validators.py`) — Pure validation functions for username, email, password, displayname formats.

### Service Layer (`app/service/`)

Use cases / business logic. Receives dependencies via constructor injection of Core interfaces.

- `AuthService` — Login, register, activate, password reset, token refresh
- `SonglistService` — CRUD, toggle songs in playlists
- `InvitationService` — Generate, validate, toggle invitation codes
- `ReportService` — Submit song problem reports
- `UserService` — Admin user management
- `SongService` — Song CRUD, search, browse, random via local `SongRepository`
- `FileService` — Proxy to Dropbox file downloads

### Repository Layer (`app/repository/`)

SQLAlchemy 2.0 async implementations of Core repository interfaces.

- **Models** (`repository/models/`) — `DeclarativeBase` ORM models (`UserModel`, `SongListModel`, `MusicWorkModel`, `MusicVersionModel`, etc.) mapping to PostgreSQL tables in `public` schema.
- **Repositories** — Async CRUD operations, mapping between ORM models and Core entities.
- **Database** (`repository/database.py`) — Async engine and session factory.

### Infrastructure Layer (`app/infrastructure/`)

Concrete implementations of non-database Core interfaces.

- `Sha256PasswordHasher` — SHA256+salt hashing (backward compatible with legacy data)
- `JwtTokenService` — JWT access/refresh/activation/reset tokens via PyJWT
- `DropboxFileService` — PPT/sheet file download URLs from Dropbox
- `SmtpMailService` — Activation and password reset emails via SMTP

### API Layer (`app/api/`)

FastAPI routers, Pydantic schemas, and dependency injection.

- **Dependencies** (`api/dependencies.py`) — The composition root. Wires concrete implementations to services via `Depends()`. Includes `get_current_user`, `get_current_admin`, `get_current_manager` auth guards.
- **Routers** (`api/routers/`) — HTTP endpoints for health, auth, songs, songlists, admin, invitation, reports, files.
- **Schemas** (`api/schemas/`) — Pydantic request/response models.

## Key Structural Points

- **Auth**: JWT token-based (access + refresh). `OAuth2PasswordBearer` extracts Bearer token.
- **Songs are stored locally** �� Song data lives in `music_works` + `music_versions` tables (migrated from the external church-music-api MongoDB). `SqlAlchemySongRepository` provides full CRUD access.
- **Config** via `pydantic-settings.BaseSettings`, reads from `.env` and environment variables.
- **App factory**: `create_app()` in `app/__init__.py` sets up lifespan and routers.
- **Entry point**: `uvicorn app.main:app`
