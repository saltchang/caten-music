# routes/search.py

from flask import Blueprint, render_template, abort, request, redirect, current_app
from jinja2 import TemplateNotFound
from flask_login import current_user

import requests
import json

from caten_music import helper

search_bp = Blueprint("search_bp", __name__,
                      template_folder='templates')


@search_bp.route('/search')
def search():

    if current_user.is_authenticated:
        current_user.login_update()

    # 關鍵字：標題
    primary = request.args.get("primary")

    # 搜尋模式
    searchMode = request.args.get("searchMode")

    # 關鍵字：歌詞
    # lyrics = request.args.get("lyrics")

    # 關鍵字：集數
    c = request.args.get("c")
    if c != "":
        return redirect("/"), 302

    # 關鍵字：語言
    lang = request.args.get("lang")
    if lang != "":
        return redirect("/"), 302

    # 關鍵字：調性
    to = request.args.get("to")
    if to != "":
        return redirect("/"), 302
    
    apiBaseUrl = helper.CHURCH_MUSIC_API_URL

    # API 串接搜尋
    if searchMode == "title":
        requestURL = apiBaseUrl + "/api/songs/search?lang=&c=&to=&title=" + primary + "&lyrics=&test=0"
    if searchMode == "lyric":
        requestURL = apiBaseUrl + "/api/songs/search?lang=&c=&to=&lyrics=" + primary + "&title=&test=0"
    r = requests.get(requestURL)

    if not r.status_code == 200:
        result = []
    else:
        result = json.loads(r.text)

    try:
        return render_template("songs/songs.html", songs=result, songs_num=len(result), mode="search", c=c, primary=primary, searchMode=searchMode), r.status_code
    except TemplateNotFound:
        abort(404)
