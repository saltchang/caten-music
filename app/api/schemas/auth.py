from pydantic import BaseModel


class LoginRequest(BaseModel):
    primary: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    displayname: str
    password: str
    confirm_password: str
    invitation_code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class ActivateRequest(BaseModel):
    token: str


class ResendActivationRequest(BaseModel):
    email: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    password: str
    confirm_password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class CheckAvailabilityRequest(BaseModel):
    username: str | None = None
    email: str | None = None


class CheckAvailabilityResponse(BaseModel):
    username_taken: bool | None = None
    email_taken: bool | None = None
