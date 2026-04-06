from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repository.models.base import Base


class MusicWorkModel(Base):
    """A musical work (original composition) grouping related versions.

    Attributes:
        id: Primary key.
        title_original: Original title of the work.
        composer: Composer name(s).
        lyricist: Lyricist name(s).
        scripture: Related scripture reference.
        versions: All MusicVersionModel entries linked to this work.
    """

    __tablename__ = 'music_works'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title_original: Mapped[str] = mapped_column(String(255), nullable=False)
    composer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lyricist: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scripture: Mapped[str | None] = mapped_column(String(255), nullable=True)

    versions: Mapped[list[MusicVersionModel]] = relationship(  # noqa: F821
        back_populates='work',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'<MusicWorkModel id={self.id} title={self.title_original!r}>'


from app.repository.models.music_version import MusicVersionModel  # noqa: E402, F401
