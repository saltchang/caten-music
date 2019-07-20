# routes/home.py

from flask import Blueprint, render_template, abort, flash, current_app
from jinja2 import TemplateNotFound

from flask_login import current_user

import random
import requests
import json

home_bp = Blueprint("home_bp", __name__,
                    template_folder='templates')


@home_bp.route('/')
def seeHome():

    result = []

    random_amount = str(6)

    if current_user.is_authenticated:
        current_user.login_update()

        requestURL = "https://church-music-api.herokuapp.com/api/songs/random/" + random_amount
        r = requests.get(requestURL)

        if r.status_code == 200:
            result = json.loads(r.text)
            
    return render_template("pages/home.html", songs=result), 200
