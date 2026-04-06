from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class InvitationCode:
    id: int
    code: str
    created_by: int
    expires_at: datetime
    is_disabled: bool = False
    usage_count: int = 0
    last_used_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_valid(self) -> bool:
        return not self.is_disabled and datetime.now() < self.expires_at
