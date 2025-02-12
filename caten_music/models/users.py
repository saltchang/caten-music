# models/users.py

from datetime import datetime

from core.model.user import User
from core.type import IDType
from flask import current_app

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from itsdangerous import URLSafeTimedSerializer as sign

from .base import Base, db
from caten_music import helper


class UserModel(Base):
    __table_args__ = {"schema": "public"}

    # SQL Table Name
    __tablename__ = "users"

    # 資料欄位設定
    id: Mapped[IDType] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(24), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    displayname: Mapped[str] = mapped_column(String(16), nullable=False)
    register_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.today()
    )
    last_login_time: Mapped[datetime | None] = mapped_column(DateTime)
    is_authenticated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_manager: Mapped = mapped_column(Boolean, default=False)
    user_profile = relationship("UserProfile", backref="user", lazy=True)
    song_list = relationship("SongList", backref="user", lazy=True)
    song_report = relationship("SongReport", backref="user", lazy=True)

    # 定義 password 為不可讀
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    # 自動由密碼產生 hash
    @password.setter
    def password(self, password):
        self.password_hash = helper.createPasswordHash(password)

    # 使用雜湊驗算確認輸入之密碼是否正確

    def verify_password(self, password):
        return helper.checkPasswordHash(password, self.password_hash)

    # 產生帳號啟動碼

    def create_activate_token(self):
        print("====>SECRET_KEY", current_app.config["SECRET_KEY"])
        token_generator = sign(current_app.config["SECRET_KEY"])
        return token_generator.dumps({"user_id": self.id})

    # 取得用戶唯一識別碼

    def get_id(self):
        return self.username

    # 重設密碼
    def reset_pw(self, password):
        self.password_hash = helper.createPasswordHash(password)
        return self

    # 登入時更新用戶狀態資料
    def login_update(self):
        self.last_login_time = datetime.today()
        db.session.commit()
        return self

    # 註冊到資料庫

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    # 自身物件表示

    def __repr__(self):
        return "<ID: %s, Username: %s, Email: %s>" % (
            self.id,
            self.username,
            self.email,
        )

    def to_core(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            display_name=self.displayname,
            password_hash=self.password_hash,
            register_time=self.register_time,
            last_login_time=self.last_login_time,
            is_authenticated=self.is_authenticated,
            is_active=self.is_active,
            is_anonymous=self.is_anonymous,
            is_admin=self.is_admin,
            is_manager=self.is_manager,
        )
