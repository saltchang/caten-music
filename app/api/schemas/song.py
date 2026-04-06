from pydantic import BaseModel

from app.core.entities.music_version import MusicVersion


class SongResponse(BaseModel):
    """Flat song response combining MusicWork + MusicVersion fields.

    Matches the legacy API format so frontend consumers need no changes.
    """

    sid: str
    num_c: str
    num_i: str
    title: str
    title_original: str = ''
    language: str | None = None
    artist: str | None = None
    translator: str | None = None
    album: str | None = None
    tonality: str | None = None
    year: str | None = None
    lyrics: list[str] = []
    tempo: str | None = None
    time_signature: str | None = None
    publisher: str | None = None
    publisher_original: str | None = None
    composer: str | None = None
    lyricist: str | None = None
    scripture: str | None = None

    @classmethod
    def from_entity(cls, version: MusicVersion) -> SongResponse:
        """Build a SongResponse from a MusicVersion entity with work loaded.

        Args:
            version: MusicVersion entity (work should be populated).

        Returns:
            A flat SongResponse combining work and version fields.
        """
        work = version.work
        return cls(
            sid=version.sid,
            num_c=version.num_c,
            num_i=version.num_i,
            title=version.title,
            title_original=work.title_original if work else '',
            language=version.language,
            artist=version.artist,
            translator=version.translator,
            album=version.album,
            tonality=version.tonality,
            year=version.year,
            lyrics=version.lyrics or [],
            tempo=version.tempo,
            time_signature=version.time_signature,
            publisher=version.publisher,
            publisher_original=version.publisher_original,
            composer=work.composer if work else None,
            lyricist=work.lyricist if work else None,
            scripture=work.scripture if work else None,
        )
