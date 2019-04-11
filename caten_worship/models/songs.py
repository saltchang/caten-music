# models/songs.py

import caten_worship.helper as helper

def create_songs_db():
    songsDB = helper.importJSON("worshipDB.json")
    return songsDB