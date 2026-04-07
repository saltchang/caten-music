from datetime import datetime

from app.core.entities.song_report import SongReport
from app.core.entities.user import User
from app.repository.report_repository import SqlAlchemyReportRepository
from app.repository.user_repository import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_test_user(session: AsyncSession) -> User:
    repo = SqlAlchemyUserRepository(session)
    return await repo.create(
        User(
            id=0,
            username='reporter',
            email='reporter@example.com',
            password_hash='hashed_pw',
            displayname='Reporter',
            register_time=datetime(2025, 1, 1, 12, 0, 0),
        )
    )


async def test_create_report(async_session: AsyncSession):
    """
    GIVEN a valid SongReport entity linked to an existing user
    WHEN creating the report via the repository
    THEN it should persist and return the report with a generated id
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyReportRepository(async_session)
    report = SongReport(
        id=0,
        description='Broken audio link',
        song_sid='1011054',
        user_id=user.id,
        reported_time=datetime(2025, 6, 15, 10, 0, 0),
    )

    # Act
    created = await repo.create(report)

    # Assert
    assert created.id is not None
    assert created.id > 0
    assert created.description == 'Broken audio link'
    assert created.song_sid == '1011054'
    assert created.user_id == user.id


async def test_get_by_id(async_session: AsyncSession):
    """
    GIVEN a report exists in the database
    WHEN querying by id
    THEN it should return the matching report
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyReportRepository(async_session)
    report = SongReport(
        id=0,
        description='Wrong lyrics',
        song_sid='1010066',
        user_id=user.id,
        reported_time=datetime(2025, 6, 15, 10, 0, 0),
    )
    created = await repo.create(report)

    # Act
    found = await repo.get_by_id(created.id)

    # Assert
    assert found is not None
    assert found.id == created.id
    assert found.description == 'Wrong lyrics'
    assert found.song_sid == '1010066'


async def test_list_all(async_session: AsyncSession):
    """
    GIVEN two reports exist in the database
    WHEN list_all is called
    THEN both reports are returned
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyReportRepository(async_session)
    for sid in ['1011054', '1010066']:
        await repo.create(
            SongReport(
                id=0,
                description=f'Issue with {sid}',
                song_sid=sid,
                user_id=user.id,
                reported_time=datetime(2025, 6, 15, 10, 0, 0),
            )
        )

    # Act
    reports = await repo.list_all()

    # Assert
    assert len(reports) == 2


async def test_get_by_id_not_found(async_session: AsyncSession):
    """
    GIVEN no report with the given id exists
    WHEN querying by id
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemyReportRepository(async_session)

    # Act
    found = await repo.get_by_id(999)

    # Assert
    assert found is None
