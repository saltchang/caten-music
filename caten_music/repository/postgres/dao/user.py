from datetime import datetime

from sqlalchemy import select, or_, update, delete
from core.model.user import User
from core.protocol.repository.user import UserRepository

from sqlalchemy.orm import Session

from core.type import IDType
from models.users import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        existing_user = self.session.execute(
            select(UserModel).where(
                or_(
                    UserModel.username == user.username,
                    UserModel.email == user.email,
                )
            )
        ).scalar_one_or_none()

        if existing_user:
            raise ValueError("User already exists")

        new_db_user = UserModel(
            username=user.username,
            email=user.email,
            displayname=user.display_name,
            password_hash=user.password_hash,
            register_time=datetime.now(),
            last_login_time=datetime.now(),
            is_authenticated=False,
            is_active=True,
            is_anonymous=False,
            is_admin=False,
            is_manager=False,
        )

        try:
            self.session.add(new_db_user)
            self.session.commit()
            self.session.refresh(new_db_user)
            return new_db_user.to_core()
        except Exception:
            self.session.rollback()
            raise

    def get_by_id(self, user_id: IDType) -> User | None:
        db_user = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        ).scalar_one_or_none()

        return db_user.to_core() if db_user else None

    def update(self, user: User) -> User:
        self.session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                username=user.username,
                email=user.email,
                displayname=user.display_name,
            )
        )

        self.session.commit()

        return user

    def delete(self, user: User) -> None:
        self.session.execute(delete(UserModel).where(UserModel.id == user.id))
        self.session.commit()
