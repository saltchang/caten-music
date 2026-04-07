from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SongReport:
    id: int
    description: str
    song_sid: str
    user_id: int
    reported_at: datetime = field(default_factory=datetime.now)
