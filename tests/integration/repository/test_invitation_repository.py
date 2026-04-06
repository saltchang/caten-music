from datetime import datetime, timedelta

from app.core.entities.invitation_code import InvitationCode
from app.core.entities.user import User
from app.repository.invitation_repository import SqlAlchemyInvitationRepository
from app.repository.user_repository import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_test_user(session: AsyncSession) -> User:
    repo = SqlAlchemyUserRepository(session)
    return await repo.create(
        User(
            id=0,
            username='inviter',
            email='inviter@example.com',
            password_hash='hashed_pw',
            displayname='Inviter',
            register_time=datetime(2025, 1, 1, 12, 0, 0),
        )
    )


def _make_invitation(created_by: int, code: str = 'INVITE-CODE-001') -> InvitationCode:
    return InvitationCode(
        id=0,
        code=code,
        created_by=created_by,
        expires_at=datetime.now() + timedelta(days=7),
        created_at=datetime(2025, 6, 1, 12, 0, 0),
    )


async def test_create_invitation(async_session: AsyncSession):
    """
    GIVEN a valid InvitationCode entity linked to an existing user
    WHEN creating the invitation via the repository
    THEN it should persist and return the invitation with a generated id and default flags
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyInvitationRepository(async_session)
    invitation = _make_invitation(user.id)

    # Act
    created = await repo.create(invitation)

    # Assert
    assert created.id is not None
    assert created.id > 0
    assert created.code == 'INVITE-CODE-001'
    assert created.created_by == user.id
    assert created.is_disabled is False
    assert created.usage_count == 0


async def test_get_by_code(async_session: AsyncSession):
    """
    GIVEN an invitation code exists in the database
    WHEN querying by code
    THEN it should return the matching invitation
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyInvitationRepository(async_session)
    await repo.create(_make_invitation(user.id))

    # Act
    found = await repo.get_by_code('INVITE-CODE-001')

    # Assert
    assert found is not None
    assert found.code == 'INVITE-CODE-001'


async def test_get_by_code_not_found(async_session: AsyncSession):
    """
    GIVEN no invitation with the given code exists
    WHEN querying by code
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemyInvitationRepository(async_session)

    # Act
    found = await repo.get_by_code('NONEXISTENT')

    # Assert
    assert found is None


async def test_update_invitation(async_session: AsyncSession):
    """
    GIVEN an invitation code exists in the database
    WHEN updating its usage_count, is_disabled, and last_used_at fields
    THEN the returned entity and a subsequent fetch should reflect the changes
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyInvitationRepository(async_session)
    created = await repo.create(_make_invitation(user.id))

    # Act
    created.usage_count = 3
    created.is_disabled = True
    created.last_used_at = datetime(2025, 6, 10, 15, 0, 0)
    updated = await repo.update(created)

    # Assert
    assert updated.usage_count == 3
    assert updated.is_disabled is True
    assert updated.last_used_at == datetime(2025, 6, 10, 15, 0, 0)

    fetched = await repo.get_by_code('INVITE-CODE-001')
    assert fetched is not None
    assert fetched.usage_count == 3
    assert fetched.is_disabled is True


async def test_list_all(async_session: AsyncSession):
    """
    GIVEN two invitation codes exist in the database
    WHEN listing all invitations
    THEN it should return both invitation codes
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemyInvitationRepository(async_session)
    await repo.create(_make_invitation(user.id, code='CODE-A'))
    await repo.create(_make_invitation(user.id, code='CODE-B'))

    # Act
    invitations = await repo.list_all()

    # Assert
    assert len(invitations) == 2
    codes = {inv.code for inv in invitations}
    assert codes == {'CODE-A', 'CODE-B'}
