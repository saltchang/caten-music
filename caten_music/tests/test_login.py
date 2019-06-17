# tests/test_login.py

import pytest

from . import client, dropAll, create_test_user

dropAll()

create_test_user()

def get_login_client(client):

    client.post("/login", data=dict(
        primary="test",
        password="testpassword",
        next_url=""
    ))

    return client


def login(client, primary, password, next_url):
    """登入"""

    return client.post("/login", data=dict(
        primary=primary,
        password=password,
        next_url=next_url
    ), follow_redirects=True)


login_params = [
    ("test", "testpassword", "/surfer", "EOF templates/surfer.html", "EOF templates/login.html"),
    ("test", "testpassword", "/", "EOF templates/index.html", "EOF templates/login.html"),
    ("test2", "testpassword", "/surfer", "Wrong login imformation", "EOF templates/surfer.html"),
    ("test", "testpassword2", "/surfer", "Wrong login imformation", "EOF templates/surfer.html"),
    ("", "", "/", "Wrong login imformation", "EOF templates/index.html"),
    (None, None, "/surfer", "Play With Me", "EOF templates/surfer.html"),
    ("test_not_act", "testpasswordnotact", "/surfer", "EOF templates/account_not_activated.html", "EOF templates/surfer.html"),
    ("test", "testpassword", "/#4;:229};", "EOF templates/index.html", "EOF templates/login.html"),
]

@pytest.mark.parametrize("primary, password, next_url, ex, nex", login_params)
def test_login_post(client, primary, password, next_url, ex, nex):
    """測試登入"""

    res = login(client, primary, password, next_url)
    res = res.data.decode()

    print(res)

    assert ex in res
    assert nex not in res
