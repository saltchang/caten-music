# models/mails.py

import os

from flask_mail import Mail
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTING"))
mail = Mail(app)
