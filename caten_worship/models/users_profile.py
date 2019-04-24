# models/users_data.py

from flask import current_app

from .base import db
from caten_worship import helper


class UserProfile(db.Model):

    # SQL Table Name
    __tablename__ = "users_profile"

    # 資料欄位設定
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    about_me = db.Column(db.Text)
    phone_number = db.Column(db.String(20))

    # 預註冊到資料庫（特殊用途）

    def flush(self):
        db.session.add(self)
        db.flush()

    # 註冊到資料庫

    def save(self):
        db.session.add(self)
        db.session.commit()

    # 自身物件表示

    def __repr__(self):
        return '<ID: %s>' % (self.id)
