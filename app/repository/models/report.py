from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.models.base import Base


class SongReportModel(Base):
    __tablename__ = 'song_reports'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    song_sid: Mapped[str | None] = mapped_column(String(7), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('public.users.id'), nullable=False)
    reported_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return f'<SongReportModel id={self.id} song_sid={self.song_sid}>'
