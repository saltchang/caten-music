# tests/__init__.py

import os
import tempfile

import pytest

from caten_worship import create_app


@pytest.fixture
def client():

    app = create_app(os.environ.get("TEST_SETTING"))

    # db_fd, app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp()
    client = app.test_client()

    yield client

    # os.close(db_fd)
    # os.unlink(app.config["SQLALCHEMY_DATABASE_URI"])

# @pytest.fixture
# def get_db():

#     from caten_worship.db import db

#     yield db
