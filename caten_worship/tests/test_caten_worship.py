# tests/test_caten_worship.py

import os
import tempfile

import pytest

from caten_worship import create_app


@pytest.fixture
def client():

    app = create_app(os.environ.get("TEST_SETTING"))

    db_fd, app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config["SQLALCHEMY_DATABASE_URI"])


def test_home(client):

    # 首先測試首頁
    res = client.get("/")

    assert b'<!-- EOF templates/index.html -->' in res.data
