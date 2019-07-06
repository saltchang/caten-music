# models/report.py

from flask import current_app

from .base import db
from caten_music import helper

import datetime


class SongReport(db.Model):

    # SQL Table Name
    __tablename__ = "song_reports"

    # 資料欄位設定
    # 資料庫內 ID
    id = db.Column(db.Integer, primary_key=True)

    # 描述
    description = db.Column(db.Text)

    # 歌曲 SID
    song_sid = db.Column(db.Integer)

    # 建立者 ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 回報時間
    reported_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
        
    
    # 預註冊到資料庫（特殊用途）

    def flush(self):
        db.session.add(self)
        db.session.flush()

        return self

    # 註冊到資料庫

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    # 更新至資料庫
    def update(self):
        self.edited_time = datetime.datetime.today()
        db.session.commit()

        return self

    # 於程式運行時刷新自身物件
    def refresh(self):
        db.session.refresh(self)

        return self

    # 刪除自己
    def kill_self(self):
        db.session.delete(self)
        db.session.commit()

    # 自身物件表示
    def __repr__(self):
        return '<ID: %s>' % (self.id)
