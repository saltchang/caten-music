"""Migrate song data from MongoDB to PostgreSQL.

Reads from the church-music-api MongoDB (songs collection) and writes
into the caten-music PostgreSQL (music_works + music_versions tables).

Usage:
    uv run python scripts/migrate_mongo_to_pg.py               # full migration
    uv run python scripts/migrate_mongo_to_pg.py --dry-run     # preview only
    uv run python scripts/migrate_mongo_to_pg.py --skip-confirm  # skip prompt
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.repository.models.music_version import MusicVersionModel
from app.repository.models.music_work import MusicWorkModel

# ── Configuration ──────────────────────────────────────

CHURCH_MUSIC_API_DIR = Path(__file__).resolve().parent.parent.parent / 'church-music-api'


def load_config() -> dict[str, str]:
    """Load connection strings from .env files.

    Returns:
        Dictionary with mongo_uri, mongo_db, songs_collection,
        and postgres_url keys.

    Raises:
        SystemExit: If required environment variables are missing.
    """
    # Load church-music-api .env for MongoDB settings
    church_env = CHURCH_MUSIC_API_DIR / '.env'
    if not church_env.exists():
        print(f'Error: {church_env} not found')
        sys.exit(1)
    load_dotenv(church_env)

    mongo_uri = os.getenv('MONGO_URI', '').strip('"')
    mongo_db = os.getenv('SONGS_DB_NAME', 'caten-worship')
    songs_col = os.getenv('SONGS_COLLECTION_NAME', 'songs')

    if not mongo_uri:
        print('Error: MONGO_URI not set in church-music-api .env')
        sys.exit(1)

    # Load caten-music .env for PostgreSQL settings
    caten_env = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(caten_env, override=True)

    pg_url = os.getenv('DATABASE_URL', '')
    # Strip async driver suffix for synchronous access
    pg_url = pg_url.replace('+asyncpg', '')

    if not pg_url:
        print('Error: DATABASE_URL not set in caten-music .env')
        sys.exit(1)

    return {
        'mongo_uri': mongo_uri,
        'mongo_db': mongo_db,
        'songs_collection': songs_col,
        'postgres_url': pg_url,
    }


# ── Safety ─────────────────────────────────────────────


def confirm_target(pg_url: str) -> None:
    """Prompt user to confirm the target database before writing."""
    masked = pg_url.split('@')[-1] if '@' in pg_url else pg_url
    print(f'Target PostgreSQL: ...@{masked}')
    answer = input('確認要寫入此資料庫？(yes/no): ').strip().lower()
    if answer != 'yes':
        print('已取消遷移。')
        sys.exit(0)


# ── Song migration ─────────────────────────────────────


def build_version_fields(song: dict, work_id: int) -> dict:
    """Build MusicVersionModel field dict from a MongoDB song document.

    Args:
        song: Raw MongoDB document.
        work_id: ID of the parent MusicWorkModel.

    Returns:
        Dictionary of field name to value for MusicVersionModel.
    """
    return {
        'work_id': work_id,
        'sid': song['sid'],
        'num_c': song.get('num_c', ''),
        'num_i': song.get('num_i', ''),
        'title': song.get('title', ''),
        'language': song.get('language') or None,
        'artist': None,
        'translator': (song.get('translator', '') or '').strip() or None,
        'album': song.get('album') or None,
        'tonality': song.get('tonality') or None,
        'year': song.get('year') or None,
        'lyrics': song.get('lyrics') or None,
        'tempo': song.get('tempo') or None,
        'time_signature': song.get('time_signature') or None,
        'publisher': song.get('publisher') or None,
        'publisher_original': song.get('publisher_original') or None,
    }


def upsert_version(session: Session, fields: dict) -> str:
    """Insert or update a MusicVersionModel by sid.

    Args:
        session: Active SQLAlchemy session.
        fields: Field dict from build_version_fields().

    Returns:
        'created', 'updated', or 'unchanged'.
    """
    existing = session.execute(
        select(MusicVersionModel).where(MusicVersionModel.sid == fields['sid'])
    ).scalar_one_or_none()

    if existing is None:
        session.add(MusicVersionModel(**fields))
        return 'created'

    changed = False
    for key, value in fields.items():
        if key == 'work_id':
            continue
        if getattr(existing, key) != value:
            setattr(existing, key, value)
            changed = True
    return 'updated' if changed else 'unchanged'


def migrate_songs(session: Session, mongo_db: Database, collection_name: str, dry_run: bool) -> None:
    """Migrate songs from MongoDB to music_works + music_versions.

    Args:
        session: Active SQLAlchemy session.
        mongo_db: pymongo Database object.
        collection_name: MongoDB collection name for songs.
        dry_run: If True, show preview without committing.
    """
    songs = list(mongo_db[collection_name].find())
    print(f'[Songs] 從 MongoDB 讀取到 {len(songs)} 筆 songs')

    work_map: dict[tuple, MusicWorkModel] = {}
    stats = {'created': 0, 'updated': 0, 'unchanged': 0}

    # Load existing works to avoid duplicates
    existing_works = session.execute(select(MusicWorkModel)).scalars().all()
    for w in existing_works:
        key = (
            (w.composer or '').strip(),
            (w.lyricist or '').strip(),
        )
        work_map[key] = w

    for song in songs:
        composer = (song.get('composer', '') or '').strip()
        lyricist = (song.get('lyricist', '') or '').strip()
        title = song.get('title', '')
        translator = (song.get('translator', '') or '').strip()
        title_original = title if not translator else ''

        work_key = (composer, lyricist)

        if work_key in work_map and translator:
            work = work_map[work_key]
        else:
            work = MusicWorkModel(
                title_original=title_original or title,
                composer=composer or None,
                lyricist=lyricist or None,
                scripture=song.get('scripture') or None,
            )
            session.add(work)
            session.flush()
            work_map[work_key] = work

        fields = build_version_fields(song, work.id)
        result = upsert_version(session, fields)
        stats[result] += 1

    action = '預覽' if dry_run else '遷移'
    print(
        f'[Songs] {action}完成: '
        f'{stats["created"]} 新增, '
        f'{stats["updated"]} 更新, '
        f'{stats["unchanged"]} 無變動, '
        f'共 {len(work_map)} 個 MusicWork'
    )


# ── Main ───────────────────────────────────────────────


def main() -> None:
    """Run the MongoDB to PostgreSQL migration."""
    parser = argparse.ArgumentParser(description='MongoDB → PostgreSQL 遷移')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='預覽模式：顯示會執行的變動，但不實際寫入',
    )
    parser.add_argument(
        '--skip-confirm',
        action='store_true',
        help='跳過目標資料庫確認（僅限自動化環境）',
    )
    args = parser.parse_args()

    config = load_config()

    if not args.skip_confirm:
        confirm_target(config['postgres_url'])

    # Connect MongoDB
    mongo_client: MongoClient = MongoClient(config['mongo_uri'])
    mongo_db = mongo_client[config['mongo_db']]

    # Connect PostgreSQL (synchronous)
    pg_engine = create_engine(config['postgres_url'])

    with Session(pg_engine) as session:
        migrate_songs(session, mongo_db, config['songs_collection'], dry_run=args.dry_run)

        if args.dry_run:
            session.rollback()
            print('\n[Dry-run] 所有變動已 rollback，資料庫未被修改。')
        else:
            session.commit()
            print('\n遷移完成，所有變動已 commit。')

    mongo_client.close()
    pg_engine.dispose()


if __name__ == '__main__':
    main()
