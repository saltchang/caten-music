from dataclasses import dataclass


@dataclass
class UserProfile:
    id: int
    user_id: int
    about_me: str | None = None
    phone_number: str | None = None
    sex: str | None = None
