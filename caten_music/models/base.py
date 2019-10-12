# models/base.py

import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from caten_music import config

app = Flask(__name__)

if config == "Development":
    print("Development")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    # psycopg2.connect(dbname=os.environ.get("DB_DEV_DBNAME"), user=os.environ.get("DB_DEV_USER"), password=os.environ.get("DB_DEV_PASSWORD"), host=os.environ.get("DB_DEV_HOST"), port=os.environ.get("DB_DEV_PORT"))
elif config == "Testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
elif config == "Production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_FOR_TESTING")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)
