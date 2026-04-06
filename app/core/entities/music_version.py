from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.entities.music_work import MusicWork


@dataclass
class MusicVersion:
    """A specific version/arrangement of a musical work.

    Attributes:
        id: Primary key.
        work_id: Foreign key to the parent MusicWork.
        sid: External song identifier (e.g. '1011054').
        num_c: Collection number (e.g. '11').
        num_i: Index number within collection (e.g. '54').
        title: Title of this version.
        language: Language name (e.g. 'Chinese', 'English').
        artist: Performing artist.
        translator: Translator name(s).
        album: Album name.
        tonality: Musical key (e.g. 'G', 'Am').
        year: Year of publication/recording.
        lyrics: Lyrics lines.
        tempo: Tempo marking.
        time_signature: Time signature (e.g. '4/4').
        publisher: Publisher of this version.
        publisher_original: Original publisher name.
        work: Optional parent MusicWork, populated by repository eager loading.
    """

    id: int
    work_id: int
    sid: str
    num_c: str = ''
    num_i: str = ''
    title: str = ''
    language: str | None = None
    artist: str | None = None
    translator: str | None = None
    album: str | None = None
    tonality: str | None = None
    year: str | None = None
    lyrics: list[str] = field(default_factory=list)
    tempo: str | None = None
    time_signature: str | None = None
    publisher: str | None = None
    publisher_original: str | None = None
    work: MusicWork | None = None
