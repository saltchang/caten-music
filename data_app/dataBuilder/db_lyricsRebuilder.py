import json, sys

def checkArgs():
    if len(sys.argv) != 3:
        print("Usage: db_lyricsRebuilder.py [inputfile.json] [outputfile.json]")
    else:
        return [sys.argv[1], sys.argv[2]]

def callData(inputfile):
    try:
        inFile = open(inputfile, "r")

        inData = json.load(inFile)

        inFile.close()

        return inData
    except Exception as error:

        print(error)
        exit(1)

def rebuildLyrics(data):
    
    for song in data:
        newLyrics = []
        for p in song["lyrics"]:
            for s in p:
                newLyrics.append(s)
        song["lyrics"] = newLyrics
    
    return data


if __name__ == "__main__":
    filename = checkArgs()
    try:
        outFile = open(filename[1], "w")
    except Exception as error:
        print(error)
        exit(2)
    
    data = callData(filename[0])
    outData = rebuildLyrics(data)
    
    outFile.write(json.dumps(outData, ensure_ascii=False))
    outFile.close()

    print("Done.")
