from datetime import datetime

from pydantic import BaseModel


class SonglistCreateRequest(BaseModel):
    title: str
    song_sid: str | None = None
    is_private: bool = False


class SonglistUpdateRequest(BaseModel):
    title: str
    description: str
    is_private: bool
    is_archived: bool
    songs_sid_list: list[str]


class SonglistResponse(BaseModel):
    id: int
    out_id: str | None
    title: str | None
    description: str
    user_id: int
    songs_sid_list: list[str]
    songs_amount: int
    created_time: datetime
    edited_time: datetime
    is_private: bool
    is_archived: bool


class SonglistToggleResponse(BaseModel):
    action: str
    song_sid: str
    out_id: str
