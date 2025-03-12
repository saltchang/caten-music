.PHONY: clean, migrate-up, migrate-down, migrate-revision

MIGRATION_PATH = PYTHONPATH=./caten_music:./migrations

# Clean up build artifacts and cache
clean:
	@echo "Cleaning up..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '.ruff_cache' -exec rm -r {} +
	find . -type d -name '.mypy_cache' -exec rm -r {} +

migrate-up:
	@echo "Upgrading database to the latest migration..."
	$(MIGRATION_PATH) alembic upgrade head

migrate-down:
	@echo "Downgrading database by one migration..."
	$(MIGRATION_PATH) alembic downgrade -1

migrate-revision:
	@echo "Creating a new migration..."
	$(MIGRATION_PATH) alembic revision --autogenerate -m "$(message)"
