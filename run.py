# run.py

from caten_music import CreateApp
from flask_apscheduler import APScheduler
import datetime
import requests

app = CreateApp.Main()

def callChurchMusicAPI():
    print("Calling church-music-api...", str(datetime.datetime.now()))
    try:
        reqURL = "https://church-music-api.herokuapp.com"

        res = requests.get(reqURL)
        if res.status_code == 200:
            print("Called API successed.")
        else:
            print("Called API failed, status code:", res.status_code)
    except Exception as error:
        print("Error occurred while calling API.")
        print(error)

if __name__ == "__main__":

    scheduler = APScheduler()
    scheduler.add_job(func=callChurchMusicAPI, args=[], trigger='interval', id='callApiJob', minutes=15)
    scheduler.start()

    app.run(host='0.0.0.0')
