from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SongList:
    id: int
    user_id: int
    out_id: str | None = None
    title: str | None = None
    description: str = ''
    songs_sid_list: list[str] = field(default_factory=list)
    songs_amount: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_private: bool = False
    is_archived: bool = False

    def generate_out_id(self) -> None:
        date_str = self.created_at.strftime('%Y%m%d')
        id_part = str(self.id % 1000).zfill(3)
        self.out_id = f'{date_str}{id_part}'

    def set_default_title(self) -> None:
        if not self.title and self.out_id:
            self.title = f'未命名歌單-{self.out_id}'
