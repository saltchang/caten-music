# Commands

**Dependencies** (uses `uv`):

```bash
uv sync                    # Install dependencies
uv sync --group dev        # Include dev dependencies (ruff, colorlog)
```

**Run locally**:

```bash
python run.py              # Dev server on http://localhost:5000
```

**Lint**:

```bash
ruff check .               # Check (auto-fix enabled by default in ruff.toml)
ruff format .              # Format (single quotes, 4-space indent, 120 line length)
```

**Tests**:

```bash
pytest caten_music/tests/                    # All tests
pytest caten_music/tests/test_login.py       # Single test file
```

**Database migrations** (requires `PYTHONPATH=./caten_music:./migrations`):

```bash
make migrate-up                              # Apply latest migrations
make migrate-down                            # Revert one migration
make migrate-revision message="description"  # Generate new migration
```
