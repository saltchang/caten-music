# tests/__init__.py

import os
import time
import tempfile

import pytest


from caten_music import CreateApp


@pytest.fixture
def client():

    app = CreateApp.Test()

    # db_fd, app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp()
    client = app.test_client()

    yield client

    # os.close(db_fd)
    # os.unlink(app.config["SQLALCHEMY_DATABASE_URI"])


def dropAll():

    app = CreateApp.Test()

    from caten_music.models.base import db

    db.drop_all()


def createAll():

    app = CreateApp.Test()

    from caten_music.models.base import db

    db.create_all()


def create_test_user():

    app = CreateApp.Test()

    from caten_music import models

    models.db.create_all()

    # 建立已經啟動的帳號
    test_user = models.User(username="test", email="testmail@test.mail.commm", displayname="testDisplay", password="testpassword", is_authenticated=True, is_active=True)

    test_user.save()

    # 建立尚未啟動的帳號
    test_user_not_activated = models.User(username="test_not_act", email="testmailnotact@test.mail.commm", displayname="testDisplay", password="testpasswordnotact")

    test_user_not_activated.save()


# def create_init_db():

#     from caten_music.db import db

#     yield db
