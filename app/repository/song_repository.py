from sqlalchemy import String, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.repository.models.music_version import MusicVersionModel
from app.repository.models.music_work import MusicWorkModel


class SqlAlchemySongRepository:
    """Async SQLAlchemy implementation of the SongRepository interface.

    All query methods eagerly load the parent MusicWork relationship
    so the returned MusicVersion entities have ``work`` populated.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_sid(self, sid: str) -> MusicVersion | None:
        """Fetch a single version by its unique SID.

        Args:
            sid: External song identifier.

        Returns:
            The matching MusicVersion with work loaded, or None.
        """
        result = await self._session.execute(
            select(MusicVersionModel).options(joinedload(MusicVersionModel.work)).where(MusicVersionModel.sid == sid)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_sids(self, sids: list[str]) -> list[MusicVersion]:
        """Fetch multiple versions by their SIDs.

        Args:
            sids: List of SIDs.

        Returns:
            List of matching MusicVersion entities.
        """
        if not sids:
            return []
        result = await self._session.execute(
            select(MusicVersionModel).options(joinedload(MusicVersionModel.work)).where(MusicVersionModel.sid.in_(sids))
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def get_random(self, amount: int) -> list[MusicVersion]:
        """Fetch a random selection of song versions.

        Args:
            amount: Number of random versions to return.

        Returns:
            List of randomly selected MusicVersion entities.
        """
        result = await self._session.execute(
            select(MusicVersionModel).options(joinedload(MusicVersionModel.work)).order_by(func.random()).limit(amount)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def search(
        self,
        title: str = '',
        lyrics: str = '',
        lang: str = '',
        collection: str = '',
        tonality: str = '',
        limit: int = 50,
        offset: int = 0,
    ) -> list[MusicVersion]:
        """Search versions by various criteria with pagination.

        Args:
            title: Partial title match (case-insensitive).
            lyrics: Partial lyrics match (case-insensitive).
            lang: Exact language filter.
            collection: Exact num_c filter.
            tonality: Exact tonality filter.
            limit: Maximum number of results to return.
            offset: Number of results to skip.

        Returns:
            List of matching MusicVersion entities.
        """
        stmt = select(MusicVersionModel).options(joinedload(MusicVersionModel.work))

        if title:
            stmt = stmt.where(MusicVersionModel.title.ilike(f'%{title}%'))
        if lyrics:
            stmt = stmt.where(cast(MusicVersionModel.lyrics, String).ilike(f'%{lyrics}%'))
        if lang:
            stmt = stmt.where(MusicVersionModel.language == lang)
        if collection:
            stmt = stmt.where(MusicVersionModel.num_c == collection)
        if tonality:
            stmt = stmt.where(MusicVersionModel.tonality == tonality)

        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()]

    async def create(self, version: MusicVersion, work: MusicWork) -> MusicVersion:
        """Create a new MusicVersion, reusing an existing work if matched.

        Args:
            version: The version entity to create (id=0).
            work: The work entity (find-or-create by composer + lyricist).

        Returns:
            The persisted MusicVersion with generated id and work populated.
        """
        work_model = await self._find_or_create_work(work)
        await self._session.flush()

        version_model = MusicVersionModel(
            work_id=work_model.id,
            sid=version.sid,
            num_c=version.num_c,
            num_i=version.num_i,
            title=version.title,
            language=version.language,
            artist=version.artist,
            translator=version.translator,
            album=version.album,
            tonality=version.tonality,
            year=version.year,
            lyrics=version.lyrics or None,
            tempo=version.tempo,
            time_signature=version.time_signature,
            publisher=version.publisher,
            publisher_original=version.publisher_original,
        )
        self._session.add(version_model)
        await self._session.flush()
        await self._session.commit()

        version_model.work = work_model
        return self._to_entity(version_model)

    async def delete(self, sid: str) -> bool:
        """Delete a MusicVersion by its SID.

        Args:
            sid: External song identifier.

        Returns:
            True if the version was found and deleted, False otherwise.
        """
        result = await self._session.execute(select(MusicVersionModel).where(MusicVersionModel.sid == sid))
        model = result.scalars().first()
        if model is None:
            return False

        await self._session.delete(model)
        await self._session.flush()
        await self._session.commit()
        return True

    async def update(self, version: MusicVersion) -> MusicVersion:
        """Update an existing MusicVersion.

        Args:
            version: The version entity with updated fields.

        Returns:
            The updated MusicVersion entity.

        Raises:
            ValueError: If the version id is not found.
        """
        result = await self._session.execute(
            select(MusicVersionModel)
            .options(joinedload(MusicVersionModel.work))
            .where(MusicVersionModel.id == version.id)
        )
        model = result.scalars().first()
        if model is None:
            raise ValueError(f'MusicVersion with id {version.id} not found')

        model.title = version.title
        model.language = version.language
        model.artist = version.artist
        model.translator = version.translator
        model.album = version.album
        model.tonality = version.tonality
        model.year = version.year
        model.lyrics = version.lyrics or None
        model.tempo = version.tempo
        model.time_signature = version.time_signature
        model.publisher = version.publisher
        model.publisher_original = version.publisher_original

        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def _find_or_create_work(self, work: MusicWork) -> MusicWorkModel:
        """Find an existing work by composer+lyricist or create a new one.

        Args:
            work: The work entity to match or create.

        Returns:
            The existing or newly created MusicWorkModel.
        """
        composer = (work.composer or '').strip()
        lyricist = (work.lyricist or '').strip()

        if composer or lyricist:
            stmt = select(MusicWorkModel)
            if composer:
                stmt = stmt.where(MusicWorkModel.composer == composer)
            else:
                stmt = stmt.where(MusicWorkModel.composer.is_(None))
            if lyricist:
                stmt = stmt.where(MusicWorkModel.lyricist == lyricist)
            else:
                stmt = stmt.where(MusicWorkModel.lyricist.is_(None))

            result = await self._session.execute(stmt)
            existing = result.scalars().first()
            if existing is not None:
                return existing

        model = MusicWorkModel(
            title_original=work.title_original,
            composer=composer or None,
            lyricist=lyricist or None,
            scripture=work.scripture,
        )
        self._session.add(model)
        return model

    @staticmethod
    def _to_entity(model: MusicVersionModel) -> MusicVersion:
        """Map a MusicVersionModel (with loaded work) to a domain entity.

        Args:
            model: The ORM model instance.

        Returns:
            A MusicVersion dataclass with work populated.
        """
        work_entity: MusicWork | None = None
        if model.work is not None:
            work_entity = MusicWork(
                id=model.work.id,
                title_original=model.work.title_original,
                composer=model.work.composer,
                lyricist=model.work.lyricist,
                scripture=model.work.scripture,
            )

        return MusicVersion(
            id=model.id,
            work_id=model.work_id,
            sid=model.sid,
            num_c=model.num_c,
            num_i=model.num_i,
            title=model.title,
            language=model.language,
            artist=model.artist,
            translator=model.translator,
            album=model.album,
            tonality=model.tonality,
            year=model.year,
            lyrics=model.lyrics or [],
            tempo=model.tempo,
            time_signature=model.time_signature,
            publisher=model.publisher,
            publisher_original=model.publisher_original,
            work=work_entity,
        )
