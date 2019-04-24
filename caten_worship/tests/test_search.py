# tests/test_search.py

import pytest

from . import client


def search(client, mode, scope, keyword):
    """搜尋模組"""

    return client.get("/search", query_string=dict(
        m=mode,
        s=scope,
        q=keyword), follow_redirects=True)


search_and_surf_params = [("search", "title", "來 敬拜",
                           "EOF templates/result.html", "敬拜",
                           "前", "耶穌愛我"),

                          ("search", "title", "",
                           "EOF templates/result.html", "結果", "0", "耶穌"),

                          ("xyz", "title", "來 敬拜",
                           "EOF templates/index.html", "",
                           "", "耶穌愛我"),

                          ("search", "xyz", "來 敬拜",
                           "EOF templates/result.html", "結果", "0", "耶穌"),

                          ("", "", "",
                           "EOF templates/index.html", "", "", "耶穌"),

                          ("surf", "language", "c11",
                           "EOF templates/result.html", "這世代要呼求祢",
                           "國語", "台語"),

                          ("surf", "language", "xyz",
                           "EOF templates/result.html", "共有", "0", "耶穌"),

                          ("surf", "language", "",
                           "EOF templates/result.html", "共有", "0", "耶穌"),

                          ("", "language", "c11",
                           "EOF templates/index.html", "", "", "耶穌"),

                          ("surf", "", "c11",
                           "EOF templates/index.html", "", "", "耶穌"),

                          ("surf", "xyz", "c11",
                           "EOF templates/result.html", "共有", "0", "耶穌"),
                          ]


@pytest.mark.parametrize("m, s, q, ex1, ex2, ex3, nex", search_and_surf_params)
def test_search_and_surf(client, m, s, q, ex1, ex2, ex3, nex):
    """測試搜尋功能"""

    res = search(client, m, s, q)
    res = res.data.decode()
    assert ex1 in res
    assert ex2 in res
    assert ex3 in res
    assert nex not in res
