# tests/test_static_pages.py

from . import client, create_test_user
from .test_login import get_login_client

import pytest

create_test_user()


def test_home_page(client):
    """測試首頁"""

    res = client.get("/")
    res = res.data.decode()

    assert "EOF templates/index.html" in res


def test_surfer_page(client):
    """測試瀏覽介面"""

    # 未登入
    res = client.get("/surfer", follow_redirects=True)
    res = res.data.decode()

    assert "EOF templates/login.html" in res

    # 登入
    client = get_login_client(client)

    res = client.get("/surfer", follow_redirects=True)
    res = res.data.decode()

    assert "EOF templates/surfer.html" in res


def test_register_get(client):
    """註冊頁面"""

    res = client.get("/register")
    res = res.data.decode()

    assert "EOF templates/register.html" in res


def test_login_get(client):
    """登入頁面"""

    res = client.get("/login")
    res = res.data.decode()

    assert "EOF templates/login.html" in res


def test_logout_post(client):
    """登出"""

    res = client.post("/logout", follow_redirects=True)
    res = res.data.decode()

    assert "EOF templates/index.html" in res
