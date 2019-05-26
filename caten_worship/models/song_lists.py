# models/song_lists.py

from flask import current_app

from .base import db
from caten_worship import helper

import datetime


class SongList(db.Model):

    # SQL Table Name
    __tablename__ = "song_lists"

    # 資料欄位設定
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    songs_sid_list = db.Column(db.ARRAY(db.String(8)))
    songs_amount = db.Column(db.Integer, nullable=False, default=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    edited_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    is_private = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)

    def __init__(self):
        # 建立資料時自動從日期及ID產生一組長ID
        now = datetime.datetime.today()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        if now.month < 10:
            month = "0" + month
        if now.day < 10:
            day = "0" + day
        todaystring = year + month + day + "0000"
        todayint = int(todaystring)
        self.list_id = str(todayint + self.id)
        self.title = "未命名歌單-" + self.list_id


    
    # @list_id.setter
    # def list_id(self):
        

    # @title.setter
    # def title(self):
        

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
