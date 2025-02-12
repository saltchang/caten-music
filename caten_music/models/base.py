# models/base.py

import os

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


app = current_app

with app.app_context():
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    config = os.environ.get("APP_SETTING")

    if config == "Development":
        print("Development")
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    elif config == "Testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    elif config == "Production":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)
