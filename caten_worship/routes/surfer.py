# routes/surfer.py

from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound

from flask_login import login_required

import requests
import json

surfer_bp = Blueprint("surfer_bp", __name__,
                      template_folder='templates')

surf_bp = Blueprint("surf_bp", __name__,
                      template_folder='templates')


@surfer_bp.route('/surfer')
@login_required
def surfer():

    try:
        return render_template("pages/surfer.html")
    except TemplateNotFound:
        abort(404)

@surf_bp.route('/surf')
def surf():

    # 關鍵字：標題
    title = request.args.get("title")
    if title != "":
        return redirect("/"), 400

    # 關鍵字：集數
    c = request.args.get("c").replace(" ", "")
    if c == "":
        return redirect("/"), 400

    # 關鍵字：語言
    lang = request.args.get("lang").replace(" ", "")
    if lang == "":
        return redirect("/"), 400

    # 關鍵字：調性
    to = request.args.get("to")
    if to != "":
        return redirect("/"), 400

    # API 串接 搜尋

    requestURL = "https://church-music-api.herokuapp.com/api/songs/search?lang=" + lang + "&c=" + c + "&to=&title="

    r = requests.get(requestURL)
    print("透過API瀏覽, URL:", requestURL)

    if not r.status_code == 200:
        result = []
    else:
        result = json.loads(r.text)

    try:
        return render_template("songs/result.html", songs=result, songs_num=len(result), mode="surf", c=c, lang=lang), r.status_code
    except TemplateNotFound:
        abort(404)
