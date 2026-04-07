from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repository.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(24), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    displayname: Mapped[str] = mapped_column(String(16), nullable=False)
    registered_at: Mapped[datetime] = mapped_column('register_time', DateTime, nullable=False, default=datetime.now)
    last_login_at: Mapped[datetime | None] = mapped_column('last_login_time', DateTime, nullable=True)
    is_authenticated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_manager: Mapped[bool] = mapped_column(Boolean, default=False)

    user_profile: Mapped[list[UserProfileModel]] = relationship(back_populates='user')
    song_lists: Mapped[list[SongListModel]] = relationship()
    song_reports: Mapped[list[SongReportModel]] = relationship()

    def __repr__(self) -> str:
        return f'<UserModel id={self.id} username={self.username}>'


from app.repository.models.report import SongReportModel  # noqa: E402, F401
from app.repository.models.songlist import SongListModel  # noqa: E402, F401
from app.repository.models.user_profile import UserProfileModel  # noqa: E402, F401
