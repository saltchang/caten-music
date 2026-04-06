from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repository.models.base import Base


class UserProfileModel(Base):
    __tablename__ = 'users_profile'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('public.users.id'), nullable=False)
    about_me: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sex: Mapped[str | None] = mapped_column(String(8), nullable=True)

    user: Mapped[UserModel] = relationship(back_populates='user_profile')

    def __repr__(self) -> str:
        return f'<UserProfileModel id={self.id} user_id={self.user_id}>'


from app.repository.models.user import UserModel  # noqa: E402, F401
