# helper/scheduler.py

from flask_apscheduler import APScheduler

import datetime
import requests

from .env import CHURCH_MUSIC_API_URL

def callChurchMusicAPI():
    print("Calling church-music-api...", str(datetime.datetime.now()))
    try:
        res = requests.get(CHURCH_MUSIC_API_URL + "/health")
        if res.status_code == 200:
            print("Called API successed.")
        else:
            print("Called API failed, status code:", res.status_code)
    except Exception as error:
        print("Error occurred while calling API.")
        print(error)

def handleAPISchedule():
    scheduler = APScheduler()
    scheduler.add_job(func=callChurchMusicAPI, args=[], trigger='interval', id='callApiJob', minutes=5)
    scheduler.start()
    print("Music API Scheduler start!")
    
    print("Calling church-music-api for the first time...")
    callChurchMusicAPI()
