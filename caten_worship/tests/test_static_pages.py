# tests/test_static_pages.py

from . import client


def test_home_page(client):
    """測試首頁"""

    res = client.get("/")
    res = res.data.decode()

    assert "EOF templates/index.html" in res


def test_surfer_page(client):
    """測試瀏覽介面\n
    需要登入"""

    res = client.get("/surfer", follow_redirects=True)
    res = res.data.decode()

    # db = get_db()

    assert "EOF templates/surfer.html" in res
