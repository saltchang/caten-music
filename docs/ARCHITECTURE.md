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
- `ReportService` — Submit song problem reports, list all reports (admin)
- `UserService` — Admin user management
- `SongService` — Song CRUD, unified search (with pagination), random via local `SongRepository`
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
- **Routers** (`api/routers/`) — HTTP endpoints for health, auth, songs, songlists, admin, invitation, reports, files. No `/api` prefix — this service is a dedicated API.
- **Schemas** (`api/schemas/`) — Pydantic request/response models. Response schemas use `from_entity()` classmethods to map domain entities to API responses. Request schemas use `to_*_entity()` methods to map input to domain entities at the API boundary.

## API Endpoints

All routes are mounted directly (no `/api` prefix).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Health check |
| POST | `/auth/register` | — | Register with invitation code |
| POST | `/auth/login` | — | Login, returns access + refresh tokens |
| POST | `/auth/activate` | — | Activate account via token |
| POST | `/auth/refresh` | — | Refresh tokens |
| POST | `/auth/check-availability` | — | Check username/email availability |
| POST | `/auth/forgot-password` | — | Request password reset |
| POST | `/auth/reset-password` | — | Reset password via token |
| GET | `/songs` | active user | Unified search with pagination (title, lyrics, lang, collection, tonality, limit, offset) |
| GET | `/songs/random` | active user | Random song |
| GET | `/songs/{sid}` | active user | Get song by SID |
| POST | `/songlists/` | active user | Create songlist → 201 |
| GET | `/songlists/` | active user | List user's songlists |
| GET | `/songlists/{out_id}` | active user | Get songlist detail |
| DELETE | `/songlists/{out_id}` | active user | Delete songlist |
| PATCH | `/songlists/{out_id}/songs/{sid}` | active user | Toggle song in songlist |
| POST | `/reports/` | active user | Submit song report |
| GET | `/files/ppt/{sid}` | active user | Download PPT file |
| GET | `/files/sheet/{sid}` | active user | Download sheet file |
| POST | `/admin/songs` | admin | Create song → 201 |
| PUT | `/admin/songs/{sid}` | admin | Update song, returns full resource |
| DELETE | `/admin/songs/{sid}` | admin | Delete song → 204 |
| GET | `/admin/users` | admin | List all users |
| PUT | `/admin/users/{id}` | admin | Update user role |
| GET | `/admin/reports` | admin | List all reports |
| POST | `/invitation/codes` | manager | Generate invitation code → 201 |
| PATCH | `/invitation/codes/{id}` | manager | Toggle invitation code |
| GET | `/invitation/codes` | manager | List invitation codes |
| GET | `/invitation/validate/{code}` | — | Validate invitation code |

## Key Structural Points

- **Auth**: JWT token-based (access + refresh). `OAuth2PasswordBearer` extracts Bearer token.
- **Songs are stored locally** — Song data lives in `music_works` + `music_versions` tables (migrated from the external church-music-api MongoDB). `SqlAlchemySongRepository` provides full CRUD access.
- **Service layer accepts typed entities** — Request schemas convert to domain entities at the API boundary via `to_*_entity()` methods; services never accept raw dicts.
- **Config** via `pydantic-settings.BaseSettings`, reads from `.env` and environment variables.
- **App factory**: `create_app()` in `app/__init__.py` sets up lifespan and routers.
- **Entry point**: `uvicorn app.main:app`
