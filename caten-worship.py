# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file

import os, dropbox

from importDB import importDB
from config import Config

app = Flask(__name__)

# App Configure
app.config.from_object(Config.Development)

# Database
db = importDB()

# Dropbox API
dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))

# 首頁 HomePage
@app.route("/")
def index():
    return render_template("index.html", url_for_all_songs=url_for("list_all_songs"))

# 列出所有詩歌
@app.route("/allsongs")
def list_all_songs():
    li_ = []
    li_target = []
    for i in range(len(db)):
        li_.append("ex" + str(i))
        li_target.append("#ex" + str(i))
    return render_template("all_songs.html", songs=db, li_=li_, li_target=li_target)

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
    

if __name__ == "__main__":
    app.run()
