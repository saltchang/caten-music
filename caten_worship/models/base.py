# models/base.py

import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from caten_worship import config


app = Flask(__name__)

app.config.from_object(config)

db = SQLAlchemy(app)
