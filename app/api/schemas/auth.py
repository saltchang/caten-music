from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Request body for user registration."""

    username: str
    email: str
    displayname: str
    password: str
    confirm_password: str
    invitation_code: str


class TokenResponse(BaseModel):
    """Response body containing access and refresh tokens."""

    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class ActivateRequest(BaseModel):
    """Request body for account activation."""

    token: str


class ResendActivationRequest(BaseModel):
    """Request body for resending an activation email."""

    email: str


class PasswordResetRequest(BaseModel):
    """Request body for requesting a password reset email."""

    email: str


class PasswordResetConfirm(BaseModel):
    """Request body for confirming a password reset with a new password."""

    token: str
    password: str
    confirm_password: str


class RefreshTokenRequest(BaseModel):
    """Request body for refreshing an access token."""

    refresh_token: str


class CheckAvailabilityResponse(BaseModel):
    """Response body for username/email availability checks."""

    username_taken: bool | None = None
    email_taken: bool | None = None
