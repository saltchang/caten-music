import json
import sys


def loadJsonFile():
    if len(sys.argv) == 2:
        try:
            songsdata = open(sys.argv[1], "r")
            return json.load(songsdata)
        except Exception as e:
            print(str(e))
            exit(1)
    else:
        print("Usage: db_songChecker.py [file.json]")
        exit(1)


def songChecker(songs):

    for song in songs:
        try:
            year = song["year"]
        except:
            print(song["sid"])

# Run App
if __name__ == "__main__":

    songs = loadJsonFile()

    songChecker(songs)
