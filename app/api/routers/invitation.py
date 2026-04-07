from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_admin, get_current_manager, get_invitation_service
from app.api.schemas.invitation import InvitationGenerateResponse, InvitationResponse, InvitationUpdateRequest
from app.core.entities.user import User
from app.core.exceptions import InvitationCodeDisabledError, InvitationCodeExpiredError, InvitationCodeInvalidError
from app.service.invitation_service import InvitationService

router = APIRouter(prefix='/invitation', tags=['invitation'])


@router.get('/codes', response_model=list[InvitationResponse])
async def list_codes(
    _manager: Annotated[User, Depends(get_current_manager)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    """List all invitation codes. Requires manager role.

    Args:
        _manager: Current authenticated manager (used for authorization).
        invitation_service: Injected invitation service.

    Returns:
        List of InvitationResponse for all invitation codes.
    """
    codes = await invitation_service.list_codes()
    return [InvitationResponse.from_entity(c) for c in codes]


@router.post('/codes', response_model=InvitationGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_code(
    manager: Annotated[User, Depends(get_current_manager)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    """Generate a new invitation code. Requires manager role.

    Args:
        manager: Current authenticated manager who will own the code.
        invitation_service: Injected invitation service.

    Returns:
        InvitationGenerateResponse with the newly created code.
    """
    code = await invitation_service.generate_code(manager.id)
    return InvitationGenerateResponse.from_entity(code)


@router.patch('/codes/{code_id}', response_model=InvitationResponse)
async def update_code(
    code_id: int,
    request: InvitationUpdateRequest,
    _admin: Annotated[User, Depends(get_current_admin)],
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    """Update the disabled status of an invitation code. Requires admin role.

    Args:
        code_id: ID of the invitation code to update.
        request: Payload containing the new disabled status.
        _admin: Current authenticated admin (used for authorization).
        invitation_service: Injected invitation service.

    Returns:
        InvitationResponse with the updated code.

    Raises:
        HTTPException: 400 if the invitation code is not found.
    """
    try:
        invitation = await invitation_service.update_code_status(code_id, request.is_disabled)
        return InvitationResponse.from_entity(invitation)
    except InvitationCodeInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invitation code not found') from None


@router.get('/codes/{code}', response_model=InvitationResponse)
async def get_code(
    code: str,
    invitation_service: Annotated[InvitationService, Depends(get_invitation_service)],
):
    """Validate and retrieve an invitation code by its string value.

    Args:
        code: The invitation code string to look up.
        invitation_service: Injected invitation service.

    Returns:
        InvitationResponse for the matching code.

    Raises:
        HTTPException: 404 if not found, 410 if expired or disabled.
    """
    try:
        invitation = await invitation_service.validate_code(code)
        return InvitationResponse.from_entity(invitation)
    except InvitationCodeInvalidError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invitation code not found') from None
    except InvitationCodeExpiredError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Invitation code expired') from None
    except InvitationCodeDisabledError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Invitation code is disabled') from None
