from datetime import datetime

from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, TypeDecorator, TypeEngine

from app.repository.models.base import Base


class StringArray(TypeDecorator[list[str]]):
    """ARRAY(String) on PostgreSQL, JSON on other dialects (e.g. SQLite for tests)."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[list[str]]:
        if dialect.name == 'postgresql':
            return ARRAY(String(8))  # type: ignore[return-value]
        return JSON()  # type: ignore[return-value]


class SongListModel(Base):
    __tablename__ = 'songlists'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    out_id: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    title: Mapped[str | None] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(Text, default='')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('public.users.id'), nullable=False)
    songs_sid_list: Mapped[list | None] = mapped_column(StringArray, nullable=True)
    songs_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    edited_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'<SongListModel id={self.id} out_id={self.out_id}>'
