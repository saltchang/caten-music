---
name: FastAPI refactor status
description: Tracks progress of the Flask→FastAPI+React migration and MongoDB→PostgreSQL song data migration
type: project
---

FastAPI backend refactor: all 12 phases complete (2026-04-06), 166 tests pass.

MongoDB → PostgreSQL song data migration completed (2026-04-06):
- 1,356 songs migrated from MongoDB to `music_works` (1,352 rows) + `music_versions` (1,356 rows)
- 2 API tokens migrated to `tokens` table
- Alembic migration `a0b10a05f0fe` creates the 3 new tables
- Migration script: `scripts/migrate_mongo_to_pg.py` (supports --dry-run, idempotent upsert)
- Source: church-music-api MongoDB (`caten-worship.songs` + `caten-worship.tokens`)
- `HttpxSongApiClient` is now legacy — next step is building a local SongRepository

**Why:** Consolidating all data into one PostgreSQL database to eliminate the external Go/MongoDB dependency before React frontend work begins.

**How to apply:** Song data is now local. When building song-related features, use the `music_works`/`music_versions` tables directly. The production migration will need a final re-run at deployment time to capture any data changes since this local sync.

Next steps:
- Build `SongRepository` + `SongService` to replace `HttpxSongApiClient`
- React frontend development
- Final production MongoDB → PostgreSQL migration at deployment
