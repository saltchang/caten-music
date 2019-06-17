# tests/test_search.py

import pytest

from . import client


def search(client, title, c, lang, to):
    """搜尋模組"""

    return client.get("/search", query_string=dict(
        title=title,
        c=c,
        lang=lang,
        to=to
    ), follow_redirects=True)


search_params = [("來 敬拜", "", "", "",
                  "前來敬拜",
                  "EOF templates/result.html",
                  "耶穌愛我我知道",
                  200),

                 ("", "", "", "",
                  "",
                  "EOF templates/result.html",
                  "耶穌愛我我知道",
                  400),

                 ("-999", "", "", "",
                  "",
                  "EOF templates/result.html",
                  "耶穌愛我我知道",
                  404),

                 ("敬拜", "-999", "", "",
                  "",
                  "Redirecting",
                  "敬拜",
                  400),

                 ("敬拜", "", "-999", "",
                  "",
                  "Redirecting",
                  "敬拜",
                  400),

                 ("敬拜", "", "", "-999",
                  "",
                  "Redirecting",
                  "敬拜",
                  400),

                 ]


@pytest.mark.parametrize("title, c, lang, to, ex, ex2, nex, exCode", search_params)
def test_search(client, title, c, lang, to, ex, ex2, nex, exCode):
    """測試搜尋功能"""

    res = search(client, title, c, lang, to)
    rcode = res.status_code
    res = res.data.decode()
    assert ex in res
    assert ex2 in res
    assert rcode == exCode
    assert nex not in res
