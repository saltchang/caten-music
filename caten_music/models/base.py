# models/base.py

import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from caten_music import config

app = Flask(__name__)
print("models.base")

if config == "Development":
    print("Development")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
elif config == "Testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
elif config == "Production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_FOR_TESTING")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)
