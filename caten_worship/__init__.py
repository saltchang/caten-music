# -*- coding: utf-8 -*-
import os
from flask import (Flask, jsonify, render_template,
                   request, redirect, url_for, send_file)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message


import dropbox

# Import importDB to manage songs json data
from caten_worship.importJSON import importJSON

# Import SearchEngine
from caten_worship.searchEngine import SearchCore, SurfCore

# App and Config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ.get("APP_SETTING"))

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

mail = Mail(app)
from caten_worship.poster import send_async_email, send_mail

# Database
import caten_worship.database
db = database.db
User = database.User
songsDB = importJSON("worshipDB.json")
sampleDB = importJSON("sample.json")

# Dropbox API
dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))


# 首頁
@app.route("/")
def index():
    return render_template("index.html", url_for_all_songs=url_for("list_all_songs"))

# 註冊
@app.route("/reg", methods=["GET", "POST"])
def prereg():
    username = None
    email = None
    password = None
    reg = None
    if request.method == "POST":
        email = request.values.get("email")
        username = request.values.get("username")
        password = request.values.get("password")
        reg = User(username=username, email=email, password=str(password))
        db.session.add(reg)
        db.session.commit()
        return render_template("users.html", users=db.session.query(User))
    return render_template("reg.html")


# 瀏覽所有詩歌
@app.route("/allsongs")
def list_all_songs():
    return render_template("result.html", songs=songsDB, sample=sampleDB, display_mode="allsongs")


# 下載PPT
@app.route("/download/ppt/<id_>")
def download_ppt(id_):
    try:
        result = dbx.files_get_temporary_link(
            "/caten-worship/ppt/ppt_" + id_ + ".ppt")
        return redirect(result.link)
    except Exception as e1:
        pass
    try:
        result = dbx.files_get_temporary_link(
            "/caten-worship/ppt/ppt_" + id_ + ".pptx")
        return redirect(result.link)
    except Exception as e:
        print(e)
        return "<h1>很抱歉，這首詩歌目前沒有投影片資料可供下載。<h1>", 404

# 下載歌譜
@app.route("/download/sheetmusic/<id_>")
def download_sheetmusic(id_):
    try:
        result = dbx.files_get_temporary_link(
            "/caten-worship/sheet-music/sheetmusic_" + id_ + ".jpg")
        link = result.link
        return render_template("img.html", link=link)
    except Exception as e:
        print(e)
        return "<h1>很抱歉，這首詩歌目前沒有歌譜資料可供下載。<h1>", 404

# 瀏覽
@app.route("/surfer")
def surfer():
    return render_template("surfer.html")

# 搜尋
@app.route("/search")
def searchEngine():
    mode = request.args.get("m")  # 模式 = { "search": 搜尋, "surf": 瀏覽 }
    scope = request.args.get("s")  # 範圍 = { "title": 依標題, "language": 依語言}
    keyword = request.args.get("q")  # 關鍵字

    if mode == "search" and scope:
        result = SearchCore(songsDB, scope, keyword)
    elif mode == "surf" and scope:
        result = SurfCore(songsDB, scope, keyword)
    else:
        return redirect("/")

    if not result:
        result = []
    return render_template("result.html", songs=result, songs_num=len(result), mode=mode, scope=scope, keyword=keyword)

# 回報歌曲資訊
@app.route("/report/<id_>")
def report_song(id_):
    return "你回報了id：" + str(id_) + "的歌曲資訊。"

# Email 測試
@app.route("/send/mail")
def mail_poster():
    #  主旨
    msg_title = 'Caten Worship 帳號註冊認證'
    #  寄件者，若參數有設置就不需再另外設置
    msg_sender = 'catenforjesus@gmail.com'
    #  收件者，格式為list，否則報錯
    msg_recipients = ['kk3684635@gmail.com']

    send_mail(sender=msg_sender,
              recipients=msg_recipients,
              subject=msg_title,
              template='poster.html',
              user_name='Salt')
    
    return 'You Send Message By Flask-Mail'
