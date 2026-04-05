# Architecture

This is a **Flask application** using the app factory pattern. `CreateApp` in `caten_music/__init__.py` wires everything together: it loads `.env`, selects a config file (`development.py` / `testing.py` / `production.py`) based on the `APP_SETTING` env var, then initializes models, routes (blueprints), and a background APScheduler job.

**Key structural points:**

- **Routes** (`caten_music/routes/`) — Each feature is a Flask blueprint (login, register, search, songlist, admin, surfer, etc.). `routes/__init__.py` calls `init_app()` to register all of them.
- **Models** (`caten_music/models/`) — SQLAlchemy ORM over PostgreSQL. `models/__init__.py` exposes `init_app()`. Key models: `UserModel`, `UserProfile`, `SongList`, `InvitationCode`, `SongReport`.
- **Helper** (`caten_music/helper/`) — Stateless utilities: password hashing, email token validation, registration input checks, invitation code logic, URL redirect safety (`url_defender`), and APScheduler setup.
- **Services** (`caten_music/services/`) — `mail_server.py` sends HTML emails via Flask-Mail.
- **Songs are not stored locally** — All song data is fetched from an external `CHURCH_MUSIC_API_URL` (a separate service). There is no songs table in this DB.

**Config** is selected via `APP_SETTING` env var (`Development`, `Testing`, `Production`). Tests use `CreateApp().test()` which reads `TEST_SETTING` instead and skips the scheduler.

**Migrations** use Alembic with `PYTHONPATH=./caten_music:./migrations` so that models are importable during autogeneration.
