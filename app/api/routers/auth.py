from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_auth_service
from app.api.schemas.auth import (
    ActivateRequest,
    CheckAvailabilityRequest,
    CheckAvailabilityResponse,
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResendActivationRequest,
    TokenResponse,
)
from app.api.schemas.common import MessageResponse
from app.core.exceptions import (
    EmailExistsError,
    InvalidCredentialsError,
    InvalidInputError,
    InvitationCodeDisabledError,
    InvitationCodeExpiredError,
    InvitationCodeInvalidError,
    TokenInvalidError,
    UserDeactivatedError,
    UsernameExistsError,
    UserNotActivatedError,
)
from app.service.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        result = await auth_service.login(request.primary, request.password)
        return TokenResponse(**result)
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials') from None
    except UserNotActivatedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account not activated') from None
    except UserDeactivatedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account deactivated') from None
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post('/register', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        await auth_service.register(
            username=request.username,
            email=request.email,
            displayname=request.displayname,
            password=request.password,
            confirm_password=request.confirm_password,
            invitation_code=request.invitation_code,
        )
        return MessageResponse(message='Registration successful. Please check your email to activate your account.')
    except UsernameExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists') from None
    except EmailExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists') from None
    except (InvitationCodeInvalidError, InvitationCodeExpiredError, InvitationCodeDisabledError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post('/activate', response_model=MessageResponse)
async def activate(
    request: ActivateRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        await auth_service.activate_account(request.token)
        return MessageResponse(message='Account activated successfully')
    except TokenInvalidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired activation token'
        ) from None


@router.post('/resend-activation', response_model=MessageResponse)
async def resend_activation(
    request: ResendActivationRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        await auth_service.resend_activation_email(request.email)
        return MessageResponse(message='Activation email sent if the account exists')
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post('/request-password-reset', response_model=MessageResponse)
async def request_password_reset(
    request: PasswordResetRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    await auth_service.request_password_reset(request.email)
    return MessageResponse(message='Password reset email sent if the account exists')


@router.post('/reset-password', response_model=MessageResponse)
async def reset_password(
    request: PasswordResetConfirm,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        await auth_service.reset_password(request.token, request.password, request.confirm_password)
        return MessageResponse(message='Password reset successfully')
    except TokenInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired reset token') from None
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post('/refresh', response_model=TokenResponse)
async def refresh(
    request: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        result = await auth_service.refresh_token(request.refresh_token)
        return TokenResponse(**result)
    except TokenInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid refresh token') from None


@router.post('/check-availability', response_model=CheckAvailabilityResponse)
async def check_availability(
    request: CheckAvailabilityRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await auth_service.check_availability(
        username=request.username,
        email=request.email,
    )
    return CheckAvailabilityResponse(**result)
