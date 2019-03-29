# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, redirect, url_for

import os, dropbox

from importDB import importDB
from config import Config

app = Flask(__name__)

app.config.from_object(Config.Production)

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

if __name__ == "__main__":
    app.run()
