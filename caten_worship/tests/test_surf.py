# tests/test_surf.py

import pytest

from . import client


def surf(client, title, c, lang, to):
    """搜尋模組"""

    return client.get("/surf", query_string=dict(
        title=title,
        c=c,
        lang=lang,
        to=to
    ), follow_redirects=True)


surf_params = [("", "10", "Chinese", "",
                "前來敬拜",
                "EOF templates/result.html",
                "耶穌愛我我知道",
                200),

               ("", "", "", "",
                "",
                "Redirecting",
                "前來敬拜",
                400),

               ("", "10", "", "",
                "",
                "Redirecting",
                "前來敬拜",
                400),

               ("", "", "Chinese", "",
                "",
                "Redirecting",
                "前來敬拜",
                400),

               ("敬拜", "10", "Chinese", "",
                "",
                "Redirecting",
                "敬拜",
                400),

               ("", "10", "Chinese", "G",
                "",
                "Redirecting",
                "敬拜",
                400),

               ]


@pytest.mark.parametrize("title, c, lang, to, ex, ex2, nex, exCode", surf_params)
def test_surf(client, title, c, lang, to, ex, ex2, nex, exCode):
    """測試搜尋功能"""

    res = surf(client, title, c, lang, to)
    rcode = res.status_code
    res = res.data.decode()
    assert ex in res
    assert ex2 in res
    assert rcode == exCode
    assert nex not in res
