from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy

import os
import dropbox

from importDB import importDB
from searchEngine import SearchCore
from config import Config

app = Flask(__name__)

# App Configure
app.config.from_object(Config.Development)

# Database
db = SQLAlchemy(app)
jsonDB = importDB("worshipDB.json")
db_sample = importDB("sample.json")

# Dropbox API
dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))

# 建立DB物件
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email
    
    def __repr__(self):
        return "<E-mail %r>" % self.email

# 首頁
@app.route("/")
def index():
    return render_template("index.html", url_for_all_songs=url_for("list_all_songs"))

# 註冊
@app.route("/reg", methods=["GET" ,"POST"])
def prereg():
    email = None
    if request.method == "POST":
        email = request.form["email"]
        # 檢查 email 是否已存在？
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template("users.html", users=db.session.query(User))
    return render_template("reg.html")


# 瀏覽所有詩歌
@app.route("/allsongs")
def list_all_songs():
    return render_template("result.html", songs=jsonDB, sample=db_sample, display_mode="allsongs")

# 下載PPT
@app.route("/download/ppt/<id_>")
def download_ppt(id_):
    try:
        result = dbx.files_get_temporary_link("/caten-worship/ppt/ppt_" + id_ + ".ppt")
        return redirect(result.link)
    except Exception as e:
        print(e)
        return "<h1>很抱歉，這首詩歌目前沒有投影片資料可供下載。<h1>", 404

# 下載歌譜
@app.route("/download/sheetmusic/<id_>")
def download_sheetmusic(id_):
    try:  
        result = dbx.files_get_temporary_link("/caten-worship/sheet-music/sheetmusic_" + id_ + ".jpg")
        link = result.link
        return render_template("img.html", link=link)
    except Exception as e:
        print(e)
        return "<h1>很抱歉，這首詩歌目前沒有歌譜資料可供下載。<h1>", 404

# 搜尋引擎
@app.route("/search")
def searchEngine():
    searchMethod = "title"
    keyword = request.args.get("q")
    result = SearchCore(jsonDB, "title", keyword)
    if result:
        return render_template("result.html", keyword=keyword, songs=result, songs_num=len(result), display_mode="search")
    else:
        return render_template("result.html", keyword=keyword, songs=[], songs_num=0, display_mode="search")

# 回報歌曲資訊
@app.route("/report/<id_>")
def report_song(id_):
    return "你回報了id：" + str(id_) + "的歌曲資訊。"
    

if __name__ == "__main__":
    app.run()
