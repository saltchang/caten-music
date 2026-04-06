from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.songlist import SongList
from app.repository.models.songlist import SongListModel


class SqlAlchemySonglistRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_out_id(self, out_id: str) -> SongList | None:
        result = await self._session.execute(select(SongListModel).where(SongListModel.out_id == out_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_user_id(self, user_id: int) -> list[SongList]:
        result = await self._session.execute(select(SongListModel).where(SongListModel.user_id == user_id))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, songlist: SongList) -> SongList:
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
        model.created_time = songlist.created_time
        model.edited_time = songlist.edited_time
        model.is_private = songlist.is_private
        model.is_archived = songlist.is_archived
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def delete(self, songlist_id: int) -> None:
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
            created_time=model.created_time,
            edited_time=model.edited_time,
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
            created_time=songlist.created_time,
            edited_time=songlist.edited_time,
            is_private=songlist.is_private,
            is_archived=songlist.is_archived,
        )
