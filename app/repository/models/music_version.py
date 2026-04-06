from sqlalchemy import ARRAY, ForeignKey, Integer, String, Text
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, TypeDecorator, TypeEngine

from app.repository.models.base import Base


class TextArray(TypeDecorator[list[str]]):
    """ARRAY(Text) on PostgreSQL, JSON on other dialects (e.g. SQLite for tests)."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[list[str]]:
        if dialect.name == 'postgresql':
            return ARRAY(Text)  # type: ignore[return-value]
        return JSON()  # type: ignore[return-value]


class MusicVersionModel(Base):
    """A specific version/arrangement of a musical work.

    Attributes:
        id: Primary key.
        work_id: Foreign key to the parent MusicWork.
        sid: External song identifier (unique, e.g. '1011054').
        num_c: Collection number (string, e.g. '11').
        num_i: Index number within collection (string, e.g. '54').
        title: Title of this version.
        language: Language name (e.g. 'Chinese', 'English').
        artist: Performing artist.
        translator: Translator name(s).
        album: Album name.
        tonality: Musical key (e.g. 'G', 'Am').
        year: Year of publication/recording (string).
        lyrics: Lyrics lines stored as a text array.
        tempo: Tempo marking.
        time_signature: Time signature (e.g. '4/4').
        publisher: Publisher of this version.
        publisher_original: Original publisher name.
        work: Parent MusicWorkModel relationship.
    """

    __tablename__ = 'music_versions'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work_id: Mapped[int] = mapped_column(Integer, ForeignKey('public.music_works.id'), nullable=False, index=True)
    sid: Mapped[str] = mapped_column(String(7), unique=True, nullable=False, index=True)
    num_c: Mapped[str] = mapped_column(String(3), nullable=False)
    num_i: Mapped[str] = mapped_column(String(3), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    artist: Mapped[str | None] = mapped_column(String(255), nullable=True)
    translator: Mapped[str | None] = mapped_column(String(255), nullable=True)
    album: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tonality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    year: Mapped[str | None] = mapped_column(String(10), nullable=True)
    lyrics: Mapped[list[str] | None] = mapped_column(TextArray, nullable=True)
    tempo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    time_signature: Mapped[str | None] = mapped_column(String(20), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publisher_original: Mapped[str | None] = mapped_column(String(255), nullable=True)

    work: Mapped[MusicWorkModel] = relationship(  # noqa: F821
        back_populates='versions',
    )

    def __repr__(self) -> str:
        return f'<MusicVersionModel id={self.id} sid={self.sid!r} title={self.title!r}>'


from app.repository.models.music_work import MusicWorkModel  # noqa: E402, F401
