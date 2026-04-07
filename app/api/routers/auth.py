from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_auth_service
from app.api.schemas.auth import (
    ActivateRequest,
    CheckAvailabilityResponse,
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Authenticate a user and return access and refresh tokens.

    Args:
        form_data: OAuth2 form with username and password.
        auth_service: Injected authentication service.

    Returns:
        TokenResponse with access and refresh tokens.

    Raises:
        HTTPException: 401 if credentials are invalid, 403 if account is not
            activated or deactivated, 400 for other input errors.
    """
    try:
        result = await auth_service.login(form_data.username, form_data.password)
        return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)
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
    """Register a new user account and send an activation email.

    Args:
        request: Registration payload including username, email, password, and
            invitation code.
        auth_service: Injected authentication service.

    Returns:
        MessageResponse confirming registration.

    Raises:
        HTTPException: 409 if username or email already exists, 400 if the
            invitation code is invalid, expired, or disabled.
    """
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
    """Activate a user account using the email activation token.

    Args:
        request: Payload containing the activation token.
        auth_service: Injected authentication service.

    Returns:
        MessageResponse confirming activation.

    Raises:
        HTTPException: 400 if the activation token is invalid or expired.
    """
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
    """Resend the account activation email.

    The response message is intentionally vague to prevent email enumeration.

    Args:
        request: Payload containing the user's email address.
        auth_service: Injected authentication service.

    Returns:
        MessageResponse indicating the email was sent if the account exists.

    Raises:
        HTTPException: 400 for invalid input.
    """
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
    """Request a password reset email.

    Always returns a success message regardless of whether the email exists
    to prevent email enumeration.

    Args:
        request: Payload containing the user's email address.
        auth_service: Injected authentication service.

    Returns:
        MessageResponse indicating the email was sent if the account exists.
    """
    await auth_service.request_password_reset(request.email)
    return MessageResponse(message='Password reset email sent if the account exists')


@router.post('/reset-password', response_model=MessageResponse)
async def reset_password(
    request: PasswordResetConfirm,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Reset a user's password using a valid reset token.

    Args:
        request: Payload containing the reset token and new password.
        auth_service: Injected authentication service.

    Returns:
        MessageResponse confirming the password was reset.

    Raises:
        HTTPException: 400 if the reset token is invalid/expired or input
            is invalid.
    """
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
    """Issue new access and refresh tokens using a valid refresh token.

    Args:
        request: Payload containing the current refresh token.
        auth_service: Injected authentication service.

    Returns:
        TokenResponse with new access and refresh tokens.

    Raises:
        HTTPException: 400 if the refresh token is invalid.
    """
    try:
        result = await auth_service.refresh_token(request.refresh_token)
        return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)
    except TokenInvalidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid refresh token') from None


@router.get('/availability', response_model=CheckAvailabilityResponse)
async def check_availability(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    username: str | None = None,
    email: str | None = None,
):
    """Check whether a username or email is already taken.

    Args:
        auth_service: Injected authentication service.
        username: Username to check. Optional.
        email: Email to check. Optional.

    Returns:
        CheckAvailabilityResponse indicating which fields are taken.
    """
    result = await auth_service.check_availability(
        username=username,
        email=email,
    )
    return CheckAvailabilityResponse(
        username_taken=result.username_taken,
        email_taken=result.email_taken,
    )
