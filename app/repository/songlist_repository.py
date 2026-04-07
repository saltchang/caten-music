from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.songlist import SongList
from app.repository.models.songlist import SongListModel


class SqlAlchemySonglistRepository:
    """SQLAlchemy repository for SongList entities backed by PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self._session = session

    async def get_by_out_id(self, out_id: str) -> SongList | None:
        """Fetch a songlist by its external identifier.

        Args:
            out_id: The public-facing songlist identifier.

        Returns:
            The matching SongList entity, or None if not found.
        """
        result = await self._session.execute(select(SongListModel).where(SongListModel.out_id == out_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_user_id(self, user_id: int) -> list[SongList]:
        """Fetch all songlists belonging to a user.

        Args:
            user_id: The owning user's primary key.

        Returns:
            List of SongList entities for the user.
        """
        result = await self._session.execute(select(SongListModel).where(SongListModel.user_id == user_id))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, songlist: SongList) -> SongList:
        """Persist a new songlist, generating its out_id and default title.

        Args:
            songlist: The SongList entity to create.

        Returns:
            The persisted SongList with generated id, out_id, and title.
        """
        model = self._to_model(songlist)
        self._session.add(model)
        await self._session.flush()

        entity = self._to_entity(model)
        entity.generate_out_id()
        entity.set_default_title()

        model.out_id = entity.out_id
        model.title = entity.title
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def update(self, songlist: SongList) -> SongList:
        """Update an existing songlist.

        Args:
            songlist: The SongList entity with updated fields.

        Returns:
            The updated SongList entity.

        Raises:
            ValueError: If the songlist id is not found.
        """
        result = await self._session.execute(select(SongListModel).where(SongListModel.id == songlist.id))
        model = result.scalars().first()
        if model is None:
            raise ValueError(f'SongList with id {songlist.id} not found')
        model.out_id = songlist.out_id
        model.title = songlist.title
        model.description = songlist.description
        model.user_id = songlist.user_id
        model.songs_sid_list = songlist.songs_sid_list
        model.songs_amount = songlist.songs_amount
        model.created_at = songlist.created_at
        model.updated_at = songlist.updated_at
        model.is_private = songlist.is_private
        model.is_archived = songlist.is_archived
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def delete(self, songlist_id: int) -> None:
        """Delete a songlist by its primary key.

        Does nothing if the songlist does not exist.

        Args:
            songlist_id: Primary key of the songlist to delete.
        """
        result = await self._session.execute(select(SongListModel).where(SongListModel.id == songlist_id))
        model = result.scalars().first()
        if model is not None:
            await self._session.delete(model)
            await self._session.commit()

    @staticmethod
    def _to_entity(model: SongListModel) -> SongList:
        return SongList(
            id=model.id,
            user_id=model.user_id,
            out_id=model.out_id,
            title=model.title,
            description=model.description or '',
            songs_sid_list=model.songs_sid_list or [],
            songs_amount=model.songs_amount,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_private=model.is_private,
            is_archived=model.is_archived,
        )

    @staticmethod
    def _to_model(songlist: SongList) -> SongListModel:
        return SongListModel(
            user_id=songlist.user_id,
            out_id=songlist.out_id,
            title=songlist.title,
            description=songlist.description,
            songs_sid_list=songlist.songs_sid_list,
            songs_amount=songlist.songs_amount,
            created_at=songlist.created_at,
            updated_at=songlist.updated_at,
            is_private=songlist.is_private,
            is_archived=songlist.is_archived,
        )
