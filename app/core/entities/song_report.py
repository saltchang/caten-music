from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SongReport:
    id: int
    description: str
    song_sid: int
    user_id: int
    reported_time: datetime = field(default_factory=datetime.now)
