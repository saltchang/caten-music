# models/song_lists.py

from flask import current_app

from .base import db
from caten_music import helper

import datetime


class SongList(db.Model):

    __table_args__ = {"schema": "public"}

    # SQL Table Name
    __tablename__ = "songlists"

    # 資料欄位設定
    # 資料庫內 ID
    id = db.Column(db.Integer, primary_key=True)
    
    # 歌單對外 ID
    out_id = db.Column(db.String(32), unique=True)

    # 標題
    title = db.Column(db.String(32))

    # 描述
    description = db.Column(db.Text, default="")

    # 建立者 ID
    user_id = db.Column(db.Integer, db.ForeignKey('public.users.id'),
        nullable=False)
    
    # 歌單所存放歌曲之SID
    songs_sid_list = db.Column(db.ARRAY(db.String(8)))

    # 歌曲數量
    songs_amount = db.Column(db.Integer, nullable=False, default=0)

    # 建立時間
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())

    # 最後更新時間
    edited_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())

    # 隱私設定
    is_private = db.Column(db.Boolean, default=False)

    # 是否封存
    is_archived = db.Column(db.Boolean, default=False)

    # 預設設定
    def init(self):

        # 建立資料時自動從日期及ID產生一組長ID
        now = self.created_time

        year = str(now.year)
        
        month = str(now.month)
        if now.month < 10:
            month = "0" + month
        
        day = str(now.day)
        if now.day < 10:
            day = "0" + day
        
        hour = str(now.hour)
        if now.hour < 10:
            hour = "0" + day
        
        minute = str(now.minute)
        if now.minute < 10:
            minute = "0" + day
        
        second = str(now.second)
        if now.second < 10:
            second = "0" + day 
        todaystring = year + month + day + "000"

        todayint = int(todaystring)

        id_to_add = self.id % 1000

        self.out_id = str(todayint + id_to_add)

        # 如果使用者沒有輸入標題，則設定為預設值
        if self.title == "":
            self.title = "未命名歌單-" + self.out_id
        


    
    # @list_id.setter
    # def list_id(self):
        

    # @title.setter
    # def title(self):
        

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
