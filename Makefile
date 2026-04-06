.PHONY: dev test test-unit test-integration lint format typecheck check clean migrate-up migrate-down migrate-revision sync-db

# ── Run ──────────────────────────────────────────

dev:
	uv run uvicorn app.main:app --reload --port 3777

# ── Test ─────────────────────────────────────────

test:
	uv run pytest tests/

test-unit:
	uv run pytest tests/unit/

test-integration:
	uv run pytest tests/integration/

# ── Code Quality ─────────────────────────────────

lint:
	uv run ruff check app/ tests/

format:
	uv run ruff format app/ tests/

typecheck:
	uv run pyright

check: lint format typecheck test

# ── Database Migrations ──────────────────────────

MIGRATION_PATH = PYTHONPATH=.

migrate-up:
	$(MIGRATION_PATH) alembic upgrade head

migrate-down:
	$(MIGRATION_PATH) alembic downgrade -1

migrate-revision:
	$(MIGRATION_PATH) alembic revision --autogenerate -m "$(message)"

# ── Database ─────────────────────────────────────

sync-db:
	./scripts/sync-db.sh

# ── Misc ─────────────────────────────────────────

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '.ruff_cache' -exec rm -r {} +
	find . -type d -name '.pytest_cache' -exec rm -r {} +
