from dataclasses import dataclass


@dataclass
class MusicWork:
    """A musical work (original composition) grouping related versions.

    Attributes:
        id: Primary key.
        title_original: Original title of the work.
        composer: Composer name(s).
        lyricist: Lyricist name(s).
        scripture: Related scripture reference.
    """

    id: int
    title_original: str = ''
    composer: str | None = None
    lyricist: str | None = None
    scripture: str | None = None
