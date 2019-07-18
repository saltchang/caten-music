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
        print("Usage: db_titleChecker.py [file.json]")
        exit(1)


def titleChecker(songs):

    for song in songs:
        title = song["title"]
        
        if "：" in title:
            print(song["sid"])
            print(title)
            print()

# Run App
if __name__ == "__main__":

    songs = loadJsonFile()

    titleChecker(songs)
