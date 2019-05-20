# routes/search.py

from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound
from caten_worship import services

import requests
import json

search_bp = Blueprint("search_bp", __name__,
                      template_folder='templates')


@search_bp.route('/search')
def search():

    # 模式 = { "search": 搜尋, "surf": 瀏覽 }
    mode = request.args.get("m")

    # 範圍 = { "title": 依標題, "language": 依語言}
    scope = request.args.get("s")

    # 關鍵字
    keyword = request.args.get("q")

    # 預設 c 值
    c = ""

    # 確認 scope
    if scope:

        # 搜尋模式
        if mode == "search":
        
            # 舊版搜尋方法
            # result = services.search_songs(scope, keyword)
            # if not result:
            #     result = []

            # 新版 API 串接搜尋
            requestURL = "https://church-music-api.herokuapp.com/api/songs/search?lang=&c=&to=&title=" + keyword
            r = requests.get(requestURL)
            print("透過API搜尋, URL:", requestURL)

            if not r.status_code == 200:
                result = []
            else:
                result = json.loads(r.text)

        # 瀏覽模式
        elif mode == "surf":
            # 舊版搜尋方法
            # result = services.surf_songs(scope, keyword)

            # if not result:
            #     result = []
            #     c = ""

            # else:
            #     c = result[1]["num_c"]

            # 新版 API 串接 搜尋
            lang = keyword[0]
            if lang == "c":
                lang = "Chinese"
            elif lang == "t":
                lang = "Taiwanese"
            else:
                return redirect("/")

            c = keyword[1:]

            requestURL = "https://church-music-api.herokuapp.com/api/songs/search?lang=" + lang + "&c=" + c + "&to=&title="

            r = requests.get(requestURL)
            print("透過API瀏覽, URL:", requestURL)

            if not r.status_code == 200:
                result = []
            else:
                result = json.loads(r.text)

        else:
            return redirect("/")

    else:
        return redirect("/")

    try:
        return render_template("result.html", songs=result, songs_num=len(result), mode=mode, scope=scope, keyword=keyword, c=c)
    except TemplateNotFound:
        abort(404)
