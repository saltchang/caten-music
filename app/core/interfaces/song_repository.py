from typing import Protocol

from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork


class SongRepository(Protocol):
    """Repository interface for song data (MusicWork + MusicVersion).

    All query methods return MusicVersion entities with the ``work``
    association populated via eager loading.
    """

    async def get_by_sid(self, sid: str) -> MusicVersion | None:
        """Fetch a single version by its unique SID.

        Args:
            sid: External song identifier (e.g. '1010066').

        Returns:
            The matching MusicVersion with work loaded, or None.
        """
        ...

    async def get_by_sids(self, sids: list[str]) -> list[MusicVersion]:
        """Fetch multiple versions by their SIDs.

        Args:
            sids: List of SIDs.

        Returns:
            List of matching MusicVersion entities.
        """
        ...

    async def get_random(self, amount: int) -> list[MusicVersion]:
        """Fetch a random selection of song versions.

        Args:
            amount: Number of random versions to return.

        Returns:
            List of randomly selected MusicVersion entities.
        """
        ...

    async def search(
        self,
        title: str = '',
        lyrics: str = '',
        lang: str = '',
        collection: str = '',
        tonality: str = '',
    ) -> list[MusicVersion]:
        """Search versions by various criteria.

        Args:
            title: Partial title match (case-insensitive).
            lyrics: Partial lyrics match (case-insensitive).
            lang: Exact language filter.
            collection: Exact num_c (collection number) filter.
            tonality: Exact tonality filter.

        Returns:
            List of matching MusicVersion entities.
        """
        ...

    async def create(self, version: MusicVersion, work: MusicWork) -> MusicVersion:
        """Create a new MusicVersion with its parent MusicWork.

        If a matching work already exists (same composer + lyricist),
        the version is linked to the existing work.

        Args:
            version: The version entity to create (id=0).
            work: The work entity (used for find-or-create).

        Returns:
            The persisted MusicVersion with generated id and work populated.
        """
        ...

    async def delete(self, sid: str) -> bool:
        """Delete a MusicVersion by its SID.

        Args:
            sid: External song identifier.

        Returns:
            True if the version was found and deleted, False otherwise.
        """
        ...

    async def update(self, version: MusicVersion) -> MusicVersion:
        """Update an existing MusicVersion.

        Args:
            version: The version entity with updated fields.

        Returns:
            The updated MusicVersion entity.
        """
        ...
