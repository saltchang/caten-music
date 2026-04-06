from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.repository.song_repository import SqlAlchemySongRepository
from sqlalchemy.ext.asyncio import AsyncSession


def _make_work(
    title_original: str = '我獻上我心',
    composer: str | None = 'Reuben Morgan',
    lyricist: str | None = 'Reuben Morgan',
    scripture: str | None = None,
) -> MusicWork:
    return MusicWork(
        id=0,
        title_original=title_original,
        composer=composer,
        lyricist=lyricist,
        scripture=scripture,
    )


def _make_version(
    work_id: int = 0,
    sid: str = '1011054',
    num_c: str = '11',
    num_i: str = '54',
    title: str = '我獻上我心',
    language: str | None = 'Chinese',
    translator: str | None = '周巽光',
    album: str | None = '這是真愛',
    tonality: str | None = 'G',
    lyrics: list[str] | None = None,
) -> MusicVersion:
    return MusicVersion(
        id=0,
        work_id=work_id,
        sid=sid,
        num_c=num_c,
        num_i=num_i,
        title=title,
        language=language,
        translator=translator,
        album=album,
        tonality=tonality,
        lyrics=lyrics or ['p', '我心何等渴望'],
    )


class TestCreateSong:
    async def test_create_version_with_new_work(self, async_session: AsyncSession):
        """
        GIVEN a new MusicVersion and a new MusicWork
        WHEN create is called
        THEN the version is persisted with a generated id and linked to the work
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        work = _make_work()
        version = _make_version()

        # Act
        created = await repo.create(version, work)

        # Assert
        assert created.id > 0
        assert created.sid == '1011054'
        assert created.work_id > 0
        assert created.work is not None
        assert created.work.composer == 'Reuben Morgan'

    async def test_create_version_reuses_existing_work(self, async_session: AsyncSession):
        """
        GIVEN a MusicWork already exists with the same composer and lyricist
        WHEN creating a new version with a matching work
        THEN the new version shares the same work_id as the existing version
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        work = _make_work()
        v1 = _make_version(sid='1011054')
        v2 = _make_version(sid='1011055', title='另一個版本', translator='另一位譯者')

        created_v1 = await repo.create(v1, work)

        # Act
        created_v2 = await repo.create(v2, work)

        # Assert
        assert created_v2.work_id == created_v1.work_id


class TestGetBySid:
    async def test_get_existing_song(self, async_session: AsyncSession):
        """
        GIVEN a song exists in the database
        WHEN get_by_sid is called with its SID
        THEN the matching version is returned with work populated
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(_make_version(), _make_work())

        # Act
        found = await repo.get_by_sid('1011054')

        # Assert
        assert found is not None
        assert found.sid == '1011054'
        assert found.title == '我獻上我心'
        assert found.work is not None
        assert found.work.composer == 'Reuben Morgan'

    async def test_get_nonexistent_song(self, async_session: AsyncSession):
        """
        GIVEN no song exists with the given SID
        WHEN get_by_sid is called
        THEN None is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)

        # Act
        found = await repo.get_by_sid('9999999')

        # Assert
        assert found is None


class TestGetBySids:
    async def test_get_multiple_songs(self, async_session: AsyncSession):
        """
        GIVEN two songs exist in the database
        WHEN get_by_sids is called with both SIDs
        THEN both versions are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        work = _make_work()
        await repo.create(_make_version(sid='1011054'), work)
        await repo.create(
            _make_version(sid='1010066', title='前來敬拜'),
            _make_work(title_original='前來敬拜', composer='游智婷', lyricist='游智婷'),
        )

        # Act
        found = await repo.get_by_sids(['1011054', '1010066'])

        # Assert
        assert len(found) == 2
        sids = {v.sid for v in found}
        assert sids == {'1011054', '1010066'}

    async def test_get_by_sids_partial_match(self, async_session: AsyncSession):
        """
        GIVEN only one of the requested SIDs exists
        WHEN get_by_sids is called
        THEN only the matching version is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(_make_version(sid='1011054'), _make_work())

        # Act
        found = await repo.get_by_sids(['1011054', '9999999'])

        # Assert
        assert len(found) == 1

    async def test_get_by_sids_empty_list(self, async_session: AsyncSession):
        """
        GIVEN an empty list of SIDs
        WHEN get_by_sids is called
        THEN an empty list is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)

        # Act
        found = await repo.get_by_sids([])

        # Assert
        assert found == []


class TestGetRandom:
    async def test_get_random_songs(self, async_session: AsyncSession):
        """
        GIVEN 3 songs exist in the database
        WHEN get_random(2) is called
        THEN 2 versions are returned with work populated
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        work = _make_work()
        for i in range(3):
            await repo.create(
                _make_version(sid=f'100100{i}', num_i=str(i)),
                work,
            )

        # Act
        result = await repo.get_random(2)

        # Assert
        assert len(result) == 2
        for v in result:
            assert v.work is not None

    async def test_get_random_returns_fewer_when_not_enough(self, async_session: AsyncSession):
        """
        GIVEN only 1 song exists in the database
        WHEN get_random(5) is called
        THEN only 1 version is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(_make_version(), _make_work())

        # Act
        result = await repo.get_random(5)

        # Assert
        assert len(result) == 1


class TestSearch:
    async def test_search_by_title(self, async_session: AsyncSession):
        """
        GIVEN songs with different titles exist
        WHEN search is called with a title substring
        THEN only matching versions are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(
            _make_version(sid='1011054', title='我獻上我心'),
            _make_work(title_original='我獻上我心'),
        )
        await repo.create(
            _make_version(sid='1010066', title='前來敬拜'),
            _make_work(title_original='前來敬拜', composer='游智婷', lyricist='游智婷'),
        )

        # Act
        result = await repo.search(title='獻上')

        # Assert
        assert len(result) == 1
        assert result[0].sid == '1011054'

    async def test_search_by_language(self, async_session: AsyncSession):
        """
        GIVEN songs in different languages exist
        WHEN search is called with a language filter
        THEN only matching versions are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(
            _make_version(sid='1011054', language='Chinese'),
            _make_work(),
        )
        await repo.create(
            _make_version(sid='2000001', language='English', title='I Give You My Heart'),
            _make_work(title_original='I Give You My Heart', composer='Reuben Morgan', lyricist='Reuben Morgan'),
        )

        # Act
        result = await repo.search(lang='English')

        # Assert
        assert len(result) == 1
        assert result[0].sid == '2000001'

    async def test_search_by_collection(self, async_session: AsyncSession):
        """
        GIVEN songs in different collections exist
        WHEN search is called with a collection filter
        THEN only versions with matching num_c are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(
            _make_version(sid='1011054', num_c='11'),
            _make_work(),
        )
        await repo.create(
            _make_version(sid='1020001', num_c='20', title='其他歌'),
            _make_work(title_original='其他歌', composer='其他', lyricist='其他'),
        )

        # Act
        result = await repo.search(collection='11')

        # Assert
        assert len(result) == 1
        assert result[0].num_c == '11'

    async def test_search_by_tonality(self, async_session: AsyncSession):
        """
        GIVEN songs in different tonalities exist
        WHEN search is called with a tonality filter
        THEN only matching versions are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(
            _make_version(sid='1011054', tonality='G'),
            _make_work(),
        )
        await repo.create(
            _make_version(sid='1020001', tonality='C', title='C調歌'),
            _make_work(title_original='C調歌', composer='其他', lyricist='其他'),
        )

        # Act
        result = await repo.search(tonality='G')

        # Assert
        assert len(result) == 1
        assert result[0].tonality == 'G'

    async def test_search_no_results(self, async_session: AsyncSession):
        """
        GIVEN songs exist but none match the search criteria
        WHEN search is called
        THEN an empty list is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(_make_version(), _make_work())

        # Act
        result = await repo.search(title='不存在的歌')

        # Assert
        assert result == []

    async def test_search_combined_filters(self, async_session: AsyncSession):
        """
        GIVEN songs with different attributes exist
        WHEN search is called with multiple filters
        THEN only versions matching all criteria are returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(
            _make_version(sid='1011054', language='Chinese', tonality='G'),
            _make_work(),
        )
        await repo.create(
            _make_version(sid='2000001', language='English', tonality='G', title='English Song'),
            _make_work(title_original='English Song', composer='Other', lyricist='Other'),
        )

        # Act
        result = await repo.search(lang='Chinese', tonality='G')

        # Assert
        assert len(result) == 1
        assert result[0].sid == '1011054'


class TestDeleteSong:
    async def test_delete_existing_song(self, async_session: AsyncSession):
        """
        GIVEN a song exists in the database
        WHEN delete is called with its SID
        THEN the version is removed and True is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        await repo.create(_make_version(sid='1011054'), _make_work())

        # Act
        result = await repo.delete('1011054')

        # Assert
        assert result is True
        assert await repo.get_by_sid('1011054') is None

    async def test_delete_nonexistent_song(self, async_session: AsyncSession):
        """
        GIVEN no song exists with the given SID
        WHEN delete is called
        THEN False is returned
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)

        # Act
        result = await repo.delete('9999999')

        # Assert
        assert result is False


class TestUpdateSong:
    async def test_update_version(self, async_session: AsyncSession):
        """
        GIVEN a song exists in the database
        WHEN update is called with modified fields
        THEN the changes are persisted
        """
        # Arrange
        repo = SqlAlchemySongRepository(async_session)
        created = await repo.create(_make_version(), _make_work())

        # Act
        created.tonality = 'A'
        created.album = '新專輯'
        updated = await repo.update(created)

        # Assert
        assert updated.tonality == 'A'
        assert updated.album == '新專輯'

        # Verify persistence
        fetched = await repo.get_by_sid('1011054')
        assert fetched is not None
        assert fetched.tonality == 'A'
        assert fetched.album == '新專輯'
