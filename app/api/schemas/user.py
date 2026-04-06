from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    displayname: str
    is_admin: bool
    is_manager: bool
    is_active: bool
    is_authenticated: bool


class UserUpdateRequest(BaseModel):
    displayname: str | None = None
    role: str | None = None
