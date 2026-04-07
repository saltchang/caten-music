from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.core.entities.songlist import SongList


class SonglistCreateRequest(BaseModel):
    """Request body for creating a new songlist."""

    title: str
    song_sid: str | None = None
    is_private: bool = False


class SonglistUpdateRequest(BaseModel):
    """Request body for updating an existing songlist."""

    title: str
    description: str
    is_private: bool
    is_archived: bool
    songs_sid_list: list[str]


class SonglistResponse(BaseModel):
    """Response body for songlist data."""

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

    @classmethod
    def from_entity(cls, songlist: SongList) -> SonglistResponse:
        """Build a SonglistResponse from a SongList entity.

        Args:
            songlist: SongList domain entity.

        Returns:
            A SonglistResponse with all fields mapped.
        """
        return cls(
            id=songlist.id,
            out_id=songlist.out_id,
            title=songlist.title,
            description=songlist.description,
            user_id=songlist.user_id,
            songs_sid_list=songlist.songs_sid_list,
            songs_amount=songlist.songs_amount,
            created_time=songlist.created_time,
            edited_time=songlist.edited_time,
            is_private=songlist.is_private,
            is_archived=songlist.is_archived,
        )


class SonglistToggleResponse(BaseModel):
    action: str
    song_sid: str
    out_id: str
