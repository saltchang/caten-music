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

    async def list_songs(
        self,
        title: str = '',
        lyrics: str = '',
        lang: str = '',
        collection: str = '',
        tonality: str = '',
        limit: int = 50,
        offset: int = 0,
    ) -> list[MusicVersion]:
        """Search and filter songs with pagination.

        Args:
            title: Partial title match (case-insensitive).
            lyrics: Partial lyrics match (case-insensitive).
            lang: Exact language filter.
            collection: Exact collection number filter.
            tonality: Exact tonality filter.
            limit: Maximum number of results.
            offset: Number of results to skip.

        Returns:
            List of matching MusicVersion entities.
        """
        return await self._song_repo.search(
            title=title,
            lyrics=lyrics,
            lang=lang,
            collection=collection,
            tonality=tonality,
            limit=limit,
            offset=offset,
        )

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

    async def create_song(self, version: MusicVersion, work: MusicWork) -> MusicVersion:
        """Create a new song.

        Args:
            version: MusicVersion entity to create (id=0).
            work: MusicWork entity for find-or-create.

        Returns:
            The persisted MusicVersion with generated id and work populated.
        """
        return await self._song_repo.create(version, work)

    async def delete_song(self, sid: str) -> bool:
        """Delete a song by its SID.

        Args:
            sid: SID of the song to delete.

        Returns:
            True if the song was found and deleted, False otherwise.
        """
        return await self._song_repo.delete(sid)

    async def update_song(self, sid: str, version: MusicVersion) -> MusicVersion | None:
        """Update an existing song.

        Args:
            sid: SID of the song to update.
            version: MusicVersion entity with updated fields to apply.

        Returns:
            The updated MusicVersion entity, or None if not found.
        """
        existing = await self._song_repo.get_by_sid(sid)
        if existing is None:
            return None

        existing.title = version.title if version.title else existing.title
        existing.language = version.language if version.language is not None else existing.language
        existing.artist = version.artist if version.artist is not None else existing.artist
        existing.translator = version.translator if version.translator is not None else existing.translator
        existing.album = version.album if version.album is not None else existing.album
        existing.tonality = version.tonality if version.tonality is not None else existing.tonality
        existing.year = version.year if version.year is not None else existing.year
        existing.lyrics = version.lyrics if version.lyrics else existing.lyrics
        existing.tempo = version.tempo if version.tempo is not None else existing.tempo
        existing.time_signature = (
            version.time_signature if version.time_signature is not None else existing.time_signature
        )
        existing.publisher = version.publisher if version.publisher is not None else existing.publisher
        existing.publisher_original = (
            version.publisher_original if version.publisher_original is not None else existing.publisher_original
        )

        return await self._song_repo.update(existing)
