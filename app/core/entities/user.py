from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    displayname: str
    register_time: datetime = field(default_factory=datetime.now)
    last_login_time: datetime | None = None
    is_authenticated: bool = False
    is_active: bool = True
    is_anonymous: bool = False
    is_admin: bool = False
    is_manager: bool = False
