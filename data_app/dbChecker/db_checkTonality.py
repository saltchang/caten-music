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
        print("Usage: db_checkTonality.py [file.json]")
        exit(1)


def tonalityCounter(songs):

    toList = []
    toCounter = {}

    for song in songs:
        to = song["tonality"]
        if not to in toList:
            toList.append(to)
            toCounter[to] = 1
        else:
            toCounter[to] = toCounter[to] + 1
        
        if to == "bD":
            print(song["sid"])

    print("A:" + str(toCounter["A"]))
    print("Am:" + str(toCounter["Am"]))
    print("Ab:" + str(toCounter["Ab"]))
    print("B:" + str(toCounter["B"]))
    print("Bm:" + str(toCounter["Bm"]))
    print("Bb:" + str(toCounter["Bb"]))
    print("C:" + str(toCounter["C"]))
    print("Cm:" + str(toCounter["Cm"]))
    print("C#:" + str(toCounter["C#"]))
    print("D:" + str(toCounter["D"]))
    print("Dm:" + str(toCounter["Dm"]))
    print("Db:" + str(toCounter["Db"]))
    print("E:" + str(toCounter["E"]))
    print("Em:" + str(toCounter["Em"]))
    print("Eb:" + str(toCounter["Eb"]))
    print("F:" + str(toCounter["F"]))
    print("Fm:" + str(toCounter["Fm"]))
    print("F#m:" + str(toCounter["F#m"]))
    print("G:" + str(toCounter["G"]))
    print("Gm:" + str(toCounter["Gm"]))
    print("Gm:" + str(toCounter["Gm"]))
    print("Gb:" + str(toCounter["Gb"]))
    print("None:" + str(toCounter[""]))

# Run App
if __name__ == "__main__":

    songs = loadJsonFile()

    tonalityCounter(songs)
