from dataclasses import dataclass
from datetime import datetime

from core.type import IDType


@dataclass
class User:
    id: IDType
    username: str
    email: str
    password_hash: str
    display_name: str
    register_time: datetime
    last_login_time: datetime | None
    is_authenticated: bool
    is_active: bool
    is_anonymous: bool
    is_admin: bool
    is_manager: bool
