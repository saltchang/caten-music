from typing import Any

from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.core.interfaces.song_repository import SongRepository


class SongService:
    """Service layer for song operations.

    Wraps the SongRepository to provide use-case methods for
    searching, browsing, and managing songs.

    Args:
        song_repo: Repository for song data access.
    """

    def __init__(self, song_repo: SongRepository) -> None:
        self._song_repo = song_repo

    async def search(self, mode: str, query: str) -> list[MusicVersion]:
        """Search songs by title or lyrics.

        Args:
            mode: Search mode ('title' or 'lyric').
            query: Search query string.

        Returns:
            List of matching MusicVersion entities.
        """
        if mode == 'title':
            return await self._song_repo.search(title=query)
        elif mode == 'lyric':
            return await self._song_repo.search(lyrics=query)
        return []

    async def browse(
        self,
        lang: str = '',
        collection: str = '',
        tonality: str = '',
    ) -> list[MusicVersion]:
        """Browse songs by language, collection, and tonality filters.

        Args:
            lang: Language filter.
            collection: Collection number filter.
            tonality: Tonality filter.

        Returns:
            List of matching MusicVersion entities.
        """
        return await self._song_repo.search(lang=lang, collection=collection, tonality=tonality)

    async def get_by_sid(self, sid: str) -> MusicVersion | None:
        """Get a single song by its SID.

        Args:
            sid: External song identifier.

        Returns:
            The matching MusicVersion, or None.
        """
        return await self._song_repo.get_by_sid(sid)

    async def get_by_sids(self, sids: list[str]) -> list[MusicVersion]:
        """Get multiple songs by their SIDs.

        Args:
            sids: List of SIDs.

        Returns:
            List of matching MusicVersion entities.
        """
        return await self._song_repo.get_by_sids(sids)

    async def get_random(self, amount: int = 6) -> list[MusicVersion]:
        """Get random songs.

        Args:
            amount: Number of random songs to return.

        Returns:
            List of randomly selected MusicVersion entities.
        """
        return await self._song_repo.get_random(amount)

    async def create_song(self, data: dict[str, Any]) -> str:
        """Create a new song from raw data.

        Args:
            data: Song data dictionary (matching the legacy API format).

        Returns:
            The SID of the newly created song.
        """
        work = MusicWork(
            id=0,
            title_original=data.get('title', ''),
            composer=data.get('composer') or None,
            lyricist=data.get('lyricist') or None,
            scripture=data.get('scripture') or None,
        )
        version = MusicVersion(
            id=0,
            work_id=0,
            sid=data.get('sid', ''),
            num_c=data.get('num_c', ''),
            num_i=data.get('num_i', ''),
            title=data.get('title', ''),
            language=data.get('language') or None,
            artist=data.get('artist') or None,
            translator=data.get('translator') or None,
            album=data.get('album') or None,
            tonality=data.get('tonality') or None,
            year=data.get('year') or None,
            lyrics=data.get('lyrics') or [],
            tempo=data.get('tempo') or None,
            time_signature=data.get('time_signature') or None,
            publisher=data.get('publisher') or None,
            publisher_original=data.get('publisher_original') or None,
        )
        created = await self._song_repo.create(version, work)
        return created.sid

    async def delete_song(self, sid: str) -> bool:
        """Delete a song by its SID.

        Args:
            sid: SID of the song to delete.

        Returns:
            True if the song was found and deleted, False otherwise.
        """
        return await self._song_repo.delete(sid)

    async def update_song(self, sid: str, data: dict[str, Any]) -> bool:
        """Update an existing song.

        Args:
            sid: SID of the song to update.
            data: Dictionary of fields to update.

        Returns:
            True if the song was found and updated, False otherwise.
        """
        existing = await self._song_repo.get_by_sid(sid)
        if existing is None:
            return False

        for key, value in data.items():
            if hasattr(existing, key) and key not in ('id', 'work_id', 'sid'):
                setattr(existing, key, value)

        await self._song_repo.update(existing)
        return True
