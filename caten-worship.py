# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, redirect, url_for

import os

from importDB import importDB
from config import Config

app = Flask(__name__)

app.config.from_object(Config.Production)

db = importDB()

# 首頁
@app.route("/")
def index():
    return render_template("index.html", url_for_all_songs=url_for("list_all_songs"))

@app.route("/search_engine")
def search_engine():
    func = request.args.get("function")
    keyw = request.args.get("keyword")

    if func == "by_id":
        return redirect(url_for("get_songs_by_id", id_=keyw))
    if func == "by_title":
        return redirect(url_for("get_songs_by_title", title_=keyw))
    if func == "by_tonality":
        return redirect(url_for("get_songs_by_tonality", to_=keyw))
    if func == "by_album":
        return redirect(url_for("get_songs_by_album", album_=keyw))

    return func + " " + keyw

@app.route("/allsongs")
def list_all_songs():
    return render_template("all_songs.html", songs=db)

@app.route("/get/songs/id/<id_>")
def get_songs_by_id(id_):
    try:
        for song in db:
            if song["uid"] == int(id_):
                return jsonify(song)
        return jsonify({"message": "Can't find the song by the uid: " + id_}), 400
    except Exception as e:
        return str(e), 400

@app.route("/get/songs/title/<title_>")
def get_songs_by_title(title_):
    result = []
    try:
        for song in db:
            if song["title"].find(title_) != -1:
                result.append(song)
        return jsonify(result)
        return jsonify({"message": "Can't find the song by the title: " + title_}), 400
    except Exception as e:
        return str(e), 400


@app.route("/get/songs/tonality/<to_>")
def get_songs_by_tonality(to_):
    result = []
    try:
        for song in db:
            if song["tonality"].lower().find(to_.lower()) != -1:
                result.append(song)
        return jsonify(result)
        return jsonify({"message": "Can't find the song by the tonality: " + to_}), 400
    except Exception as e:
        return str(e), 400


@app.route("/get/songs/album/<album_>")
def get_songs_by_album(album_):
    result = []
    try:
        for song in db:
            if song["album"].find(album_) != -1:
                result.append(song)
        return jsonify(result)
        return jsonify({"message": "Can't find the song by the album: " + album_}), 400
    except Exception as e:
        return str(e), 400

@app.route("/result")
def show_result():
    return render_template("result.html", searched_keyword="123", songs=db)

@app.route("/envar/test")
def envarTest():
    return "My GitHub username is " + str(os.environ.get("GITHUB_USERNAME"))

if __name__ == "__main__":
    app.run()
