# models/base.py

import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from caten_music import config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if config == "Development":
    print("Development")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_FOR_DEVELOPMENT")

elif config == "Testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_FOR_TESTING")

elif config == "Production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    

db = SQLAlchemy(app)
