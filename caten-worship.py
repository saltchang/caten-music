# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file

import os, dropbox

from importDB import importDB
from config import Config

app = Flask(__name__)

app.config.from_object(Config.Development)

db = importDB()

dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))

# 首頁 HomePage
@app.route("/")
def index():
    return render_template("index.html", url_for_all_songs=url_for("list_all_songs"))

# 列出所有詩歌
@app.route("/allsongs")
def list_all_songs():
    return render_template("all_songs.html", songs=db)

# 下載PPT
@app.route("/download/ppt/<id_>")
def download_ppt(id_):
    result = dbx.files_get_temporary_link("/caten-worship/ppt/ppt_" + id_ + ".ppt")
    return redirect(result.link)

# 下載圖片
@app.route("/download/sheetmusic/<id_>")
def download_sheetmusic(id_):
    result = dbx.files_get_temporary_link("/caten-worship/sheet-music/sheetmusic_" + id_ + ".jpg")
    link = result.link
    return render_template("img.html", link=link)

if __name__ == "__main__":
    app.run()
