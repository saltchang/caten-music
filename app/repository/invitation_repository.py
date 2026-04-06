from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.invitation_code import InvitationCode
from app.repository.models.invitation import InvitationCodeModel


class SqlAlchemyInvitationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, code_id: int) -> InvitationCode | None:
        result = await self._session.execute(select(InvitationCodeModel).where(InvitationCodeModel.id == code_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_code(self, code: str) -> InvitationCode | None:
        result = await self._session.execute(select(InvitationCodeModel).where(InvitationCodeModel.code == code))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def create(self, invitation: InvitationCode) -> InvitationCode:
        model = self._to_model(invitation)
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def update(self, invitation: InvitationCode) -> InvitationCode:
        result = await self._session.execute(select(InvitationCodeModel).where(InvitationCodeModel.id == invitation.id))
        model = result.scalars().first()
        if model is None:
            raise ValueError(f'InvitationCode with id {invitation.id} not found')
        model.code = invitation.code
        model.created_at = invitation.created_at
        model.expires_at = invitation.expires_at
        model.is_disabled = invitation.is_disabled
        model.usage_count = invitation.usage_count
        model.last_used_at = invitation.last_used_at
        model.created_by = invitation.created_by
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def list_all(self) -> list[InvitationCode]:
        result = await self._session.execute(select(InvitationCodeModel))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: InvitationCodeModel) -> InvitationCode:
        return InvitationCode(
            id=model.id,
            code=model.code,
            created_by=model.created_by,
            expires_at=model.expires_at,
            is_disabled=model.is_disabled,
            usage_count=model.usage_count,
            last_used_at=model.last_used_at,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(invitation: InvitationCode) -> InvitationCodeModel:
        return InvitationCodeModel(
            code=invitation.code,
            created_by=invitation.created_by,
            expires_at=invitation.expires_at,
            is_disabled=invitation.is_disabled,
            usage_count=invitation.usage_count,
            last_used_at=invitation.last_used_at,
            created_at=invitation.created_at,
        )
