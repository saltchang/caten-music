# routes/home.py

import json
import os

import requests
from flask import Blueprint, render_template
from flask_login import current_user

from caten_music import helper

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/')
def seeHome():
    result = []

    random_amount = str(6)

    if current_user.is_authenticated:
        current_user.login_update()

        requestURL = helper.CHURCH_MUSIC_API_URL + '/api/songs/random/' + random_amount
        r = requests.get(requestURL)

        if r.status_code == 200:
            result = json.loads(r.text)

    env_state = os.environ.get('APP_SETTING')
    return render_template('pages/home.html', songs=result, env_state=env_state), 200
