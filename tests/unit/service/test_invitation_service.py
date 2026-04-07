from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from app.core.entities.invitation_code import InvitationCode
from app.core.exceptions import (
    InvitationCodeDisabledError,
    InvitationCodeExpiredError,
    InvitationCodeInvalidError,
)
from app.service.invitation_service import InvitationService


@pytest.fixture
def invitation_repo():
    return AsyncMock()


@pytest.fixture
def service(invitation_repo):
    return InvitationService(invitation_repo=invitation_repo)


class TestGenerateCode:
    async def test_generate_creates_code(self, service, invitation_repo):
        """
        GIVEN an admin user id
        WHEN generate_code is called
        THEN a new invitation code is created and returned
        """
        # Arrange
        invitation_repo.create.return_value = InvitationCode(
            id=1,
            code='ABC123DEF456',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=48),
        )

        # Act
        result = await service.generate_code(admin_id=1)

        # Assert
        assert result.code == 'ABC123DEF456'
        invitation_repo.create.assert_called_once()


class TestValidateCode:
    async def test_valid_code(self, service, invitation_repo):
        """
        GIVEN a valid, non-expired invitation code
        WHEN validate_code is called
        THEN the invitation code entity is returned
        """
        # Arrange
        valid = InvitationCode(
            id=1,
            code='VALID123',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
        )
        invitation_repo.get_by_code.return_value = valid

        # Act
        result = await service.validate_code('VALID123')

        # Assert
        assert result.code == 'VALID123'

    async def test_nonexistent_code(self, service, invitation_repo):
        """
        GIVEN a code that does not exist in the database
        WHEN validate_code is called
        THEN InvitationCodeInvalidError is raised
        """
        # Arrange
        invitation_repo.get_by_code.return_value = None

        # Act & Assert
        with pytest.raises(InvitationCodeInvalidError):
            await service.validate_code('NOPE')

    async def test_expired_code(self, service, invitation_repo):
        """
        GIVEN an invitation code whose expiry date has passed
        WHEN validate_code is called
        THEN InvitationCodeExpiredError is raised
        """
        # Arrange
        expired = InvitationCode(
            id=1,
            code='EXPIRED',
            created_by=1,
            expires_at=datetime.now() - timedelta(hours=1),
        )
        invitation_repo.get_by_code.return_value = expired

        # Act & Assert
        with pytest.raises(InvitationCodeExpiredError):
            await service.validate_code('EXPIRED')

    async def test_disabled_code(self, service, invitation_repo):
        """
        GIVEN an invitation code that has been disabled
        WHEN validate_code is called
        THEN InvitationCodeDisabledError is raised
        """
        # Arrange
        disabled = InvitationCode(
            id=1,
            code='DISABLED',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
            is_disabled=True,
        )
        invitation_repo.get_by_code.return_value = disabled

        # Act & Assert
        with pytest.raises(InvitationCodeDisabledError):
            await service.validate_code('DISABLED')


class TestUpdateCodeStatus:
    async def test_disable_code(self, service, invitation_repo):
        """
        GIVEN an active invitation code
        WHEN update_code_status is called with is_disabled=True
        THEN the code is disabled
        """
        # Arrange
        code = InvitationCode(
            id=1,
            code='ABC',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
        )
        invitation_repo.get_by_id.return_value = code
        invitation_repo.update.return_value = code

        # Act
        result = await service.update_code_status(code_id=1, is_disabled=True)

        # Assert
        assert result.is_disabled is True

    async def test_enable_code(self, service, invitation_repo):
        """
        GIVEN a disabled invitation code
        WHEN update_code_status is called with is_disabled=False
        THEN the code is re-enabled
        """
        # Arrange
        code = InvitationCode(
            id=1,
            code='ABC',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
            is_disabled=True,
        )
        invitation_repo.get_by_id.return_value = code
        invitation_repo.update.return_value = code

        # Act
        result = await service.update_code_status(code_id=1, is_disabled=False)

        # Assert
        assert result.is_disabled is False

    async def test_update_nonexistent(self, service, invitation_repo):
        """
        GIVEN a code_id that does not exist
        WHEN update_code_status is called
        THEN InvitationCodeInvalidError is raised
        """
        # Arrange
        invitation_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(InvitationCodeInvalidError):
            await service.update_code_status(code_id=999, is_disabled=True)
