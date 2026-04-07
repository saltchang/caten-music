from pydantic import BaseModel

from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork


class SongCreateRequest(BaseModel):
    """Request body for creating a new song.

    Flat format combining MusicWork and MusicVersion fields,
    matching the API consumer's perspective.
    """

    sid: str
    num_c: str
    num_i: str
    title: str
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

    def to_version_entity(self) -> MusicVersion:
        """Map request fields to a MusicVersion entity (id=0, work_id=0).

        Returns:
            A new MusicVersion entity ready for creation.
        """
        return MusicVersion(
            id=0,
            work_id=0,
            sid=self.sid,
            num_c=self.num_c,
            num_i=self.num_i,
            title=self.title,
            language=self.language,
            artist=self.artist,
            translator=self.translator,
            album=self.album,
            tonality=self.tonality,
            year=self.year,
            lyrics=self.lyrics,
            tempo=self.tempo,
            time_signature=self.time_signature,
            publisher=self.publisher,
            publisher_original=self.publisher_original,
        )

    def to_work_entity(self) -> MusicWork:
        """Map request fields to a MusicWork entity (id=0).

        Returns:
            A new MusicWork entity for find-or-create.
        """
        return MusicWork(
            id=0,
            title_original=self.title,
            composer=self.composer,
            lyricist=self.lyricist,
            scripture=self.scripture,
        )


class SongUpdateRequest(BaseModel):
    """Request body for updating an existing song.

    All fields are optional — only provided fields are applied.
    """

    title: str | None = None
    language: str | None = None
    artist: str | None = None
    translator: str | None = None
    album: str | None = None
    tonality: str | None = None
    year: str | None = None
    lyrics: list[str] | None = None
    tempo: str | None = None
    time_signature: str | None = None
    publisher: str | None = None
    publisher_original: str | None = None

    def to_version_entity(self) -> MusicVersion:
        """Map update fields to a MusicVersion entity for partial update.

        Returns:
            A MusicVersion with only the provided fields set.
        """
        return MusicVersion(
            id=0,
            work_id=0,
            sid='',
            title=self.title or '',
            language=self.language,
            artist=self.artist,
            translator=self.translator,
            album=self.album,
            tonality=self.tonality,
            year=self.year,
            lyrics=self.lyrics or [],
            tempo=self.tempo,
            time_signature=self.time_signature,
            publisher=self.publisher,
            publisher_original=self.publisher_original,
        )


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
