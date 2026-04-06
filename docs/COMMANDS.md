# Commands

All commands are wrapped and managed in the `Makefile`. Run `make <target>` from the project root.

**Run locally**:

```bash
make dev                          # Dev server on http://localhost:3777 (auto-reload)
```

**Test**:

```bash
make test                         # All tests
make test-unit                    # Unit tests only
make test-integration             # Integration tests only
```

**Code quality**:

```bash
make lint                         # Ruff linter
make format                       # Ruff formatter
make typecheck                    # Pyright type checker
make check                        # All of the above + tests
```

**Database**:

```bash
make sync-db                                 # Dump production DB to local (reads DATABASE_URL from .env)
make migrate-up                              # Apply latest migrations
make migrate-down                            # Revert one migration
make migrate-revision message="description"  # Generate new migration
```

**Misc**:

```bash
make clean                        # Remove __pycache__, .ruff_cache, .pytest_cache
```
