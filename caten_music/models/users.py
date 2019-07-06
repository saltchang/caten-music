# models/users.py

import datetime

from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer as sign
from itsdangerous import SignatureExpired, BadSignature

from .base import db
from caten_music import helper


class User(db.Model):

    # SQL Table Name
    __tablename__ = "users"

    # 資料欄位設定
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    displayname = db.Column(db.String(16), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    last_login_time = db.Column(db.DateTime)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)
    user_profile = db.relationship('UserProfile', backref='user', lazy=True)
    song_list = db.relationship('SongList', backref='user', lazy=True)
    song_report = db.relationship('SongReport', backref='user', lazy=True)

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

    def create_activate_token(self, hours=2):
        time = hours * 3600
        token_generator = sign(
            current_app.config['SECRET_KEY'], expires_in=time)
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
        self.last_login_time = datetime.datetime.today()
        db.session.commit()
        return self

    # 預註冊到資料庫（特殊用途）

    def flush(self):
        db.session.add(self)
        db.flush()
        return self

    # 註冊到資料庫

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    # 更新至資料庫
    def update(self):
        db.session.commit()
        return self

    # 自身物件表示

    def __repr__(self):
        return '<ID: %s, Username: %s, Email: %s>' % (self.id, self.username, self.email)
