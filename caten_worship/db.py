# caten_worship/db.py

import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTING"))
db = SQLAlchemy(app)

def init_app(app):
    db.create_all()
    db.init_app(app)
