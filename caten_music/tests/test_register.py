# tests/test_register.py

import pytest

from . import client, dropAll

dropAll()


def register(client, username, email, displayname, password, confirm_password):
    """註冊"""

    return client.post("/register", data=dict(
        username=username,
        email=email,
        displayname=displayname,
        password=password,
        confirm_password=confirm_password
    ), follow_redirects=True)


register_params = [
    (None, None, None, None,
     None, "Play With Me", "EOF templates/after_register.html"),
    ("registerSuccess", "kk3684635@gmail.com", "TestDisplay", "TestPassword",
     "TestPassword", "EOF templates/after_register.html", "403"),
    ("", "", "",
     "", "", "Wrong username", "EOF templates/after_register.html"),
    ("registerFail", "", "",
     "", "", "Wrong email", "EOF templates/after_register.html"),
    ("registerFail", "registerFail@failmail.comm", "",
     "", "", "Wrong displayname", "EOF templates/after_register.html"),
    ("registerFail", "registerFail@failmail.comm", "failDisplayname",
     "", "", "Wrong password", "EOF templates/after_register.html"),
    ("registerFail", "registerFail@failmail.comm", "failDisplayname",
     "failPassword", "", "兩次輸入的密碼不一樣", "EOF templates/after_register.html"),
    ("registerSuccess", "kk3684635@gmail.com", "TestDisplay", "TestPassword",
     "TestPassword", "使用者名稱已被註冊", "EOF templates/after_register.html"),
    ("registerSuccess2", "kk3684635@gmail.com", "TestDisplay", "TestPassword",
     "TestPassword", "電子信箱已被註冊", "EOF templates/after_register.html"),
]


@pytest.mark.parametrize("username, email, displayname, password, confirm_password, ex, nex", register_params)
def test_register_post(client, username, email, displayname, password, confirm_password, ex, nex):
    """測試註冊"""

    res = register(client, username, email, displayname,
                   password, confirm_password)
    res = res.data.decode()

    print(res)

    assert ex in res
    assert nex not in res
