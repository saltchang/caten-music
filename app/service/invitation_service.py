import random
import string
from datetime import datetime, timedelta

from app.core.entities.invitation_code import InvitationCode
from app.core.exceptions import (
    InvitationCodeDisabledError,
    InvitationCodeExpiredError,
    InvitationCodeInvalidError,
)
from app.core.interfaces.invitation_repository import InvitationRepository


class InvitationService:
    def __init__(self, invitation_repo: InvitationRepository):
        self._invitation_repo = invitation_repo

    async def generate_code(self, admin_id: int, expiration_hours: int = 48) -> InvitationCode:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        invitation = InvitationCode(
            id=0,
            code=code,
            created_by=admin_id,
            expires_at=datetime.now() + timedelta(hours=expiration_hours),
        )
        return await self._invitation_repo.create(invitation)

    async def validate_code(self, code: str) -> InvitationCode:
        invitation = await self._invitation_repo.get_by_code(code)
        if not invitation:
            raise InvitationCodeInvalidError('Invalid invitation code')

        if invitation.is_disabled:
            raise InvitationCodeDisabledError('Invitation code is disabled')

        if not invitation.is_valid():
            raise InvitationCodeExpiredError('Invitation code expired')

        return invitation

    async def toggle_code(self, code_id: int, is_disabled: bool) -> InvitationCode:
        invitation = await self._invitation_repo.get_by_id(code_id)
        if not invitation:
            raise InvitationCodeInvalidError('Invitation code not found')

        invitation.is_disabled = is_disabled
        return await self._invitation_repo.update(invitation)

    async def list_codes(self) -> list[InvitationCode]:
        return await self._invitation_repo.list_all()
