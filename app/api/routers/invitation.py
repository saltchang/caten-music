from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_admin, get_invitation_service
from app.api.schemas.common import MessageResponse
from app.api.schemas.invitation import InvitationGenerateResponse, InvitationResponse, InvitationToggleRequest
from app.core.entities.user import User
from app.core.exceptions import InvitationCodeDisabledError, InvitationCodeExpiredError, InvitationCodeInvalidError
from app.service.invitation_service import InvitationService

router = APIRouter(prefix='/invitation', tags=['invitation'])


@router.get('/codes', response_model=list[InvitationResponse])
async def list_codes(
    _admin: Annotated[User, Depends(get_current_admin)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    codes = await invitation_service.list_codes()
    return [
        InvitationResponse(
            id=c.id,
            code=c.code,
            created_by=c.created_by,
            created_at=c.created_at,
            expires_at=c.expires_at,
            is_disabled=c.is_disabled,
            usage_count=c.usage_count,
        )
        for c in codes
    ]


@router.post('/codes', response_model=InvitationGenerateResponse)
async def generate_code(
    admin: Annotated[User, Depends(get_current_admin)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    code = await invitation_service.generate_code(admin.id)
    return InvitationGenerateResponse(
        id=code.id,
        code=code.code,
        expires_at=code.expires_at,
    )


@router.patch('/codes/{code_id}', response_model=MessageResponse)
async def toggle_code(
    code_id: int,
    request: InvitationToggleRequest,
    _admin: Annotated[User, Depends(get_current_admin)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    try:
        await invitation_service.toggle_code(code_id, request.is_disabled)
        action = 'disabled' if request.is_disabled else 'enabled'
        return MessageResponse(message=f'Invitation code {action} successfully')
    except InvitationCodeInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invitation code not found') from None


@router.get('/validate/{code}', response_model=MessageResponse)
async def validate_code(
    code: str,
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    try:
        await invitation_service.validate_code(code)
        return MessageResponse(message='Invitation code is valid')
    except InvitationCodeInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid invitation code') from None
    except InvitationCodeExpiredError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invitation code expired') from None
    except InvitationCodeDisabledError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invitation code is disabled') from None
