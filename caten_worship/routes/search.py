# routes/search.py

from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound
from caten_worship import services

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
            result = services.search_songs(scope, keyword)

            if not result:
                result = []

        # 瀏覽模式
        elif mode == "surf":
            result = services.surf_songs(scope, keyword)

            if not result:
                result = []
                c = ""

            else:
                c = result[1]["num_c"]

        else:
            return redirect("/")

    else:
        return redirect("/")

    try:
        return render_template("result.html", songs=result, songs_num=len(result), mode=mode, scope=scope, keyword=keyword, c=c)
    except TemplateNotFound:
        abort(404)
