# tests/test_search.py

from caten_worship.tests.test_caten_worship import client


def search(client, mode, scope, keyword):

    return client.get("/search", query_string=dict(
        m=mode, 
        s=scope, 
        q=keyword), follow_redirects=True)

def test_search(client):
    # 測試搜尋功能

    res = search(client, "search", "title", "來 敬拜")
    res = res.data.decode()
    assert '<!-- EOF templates/result.html -->' in res
    assert '龍' not in res
    assert '來' in res
    assert '敬拜' in res
