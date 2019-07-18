import json
import sys


def argsCheck():
    def usageMessage():
        print("Usage: db_matcher.py [option]")
        print("option: - relative")
        print("        - full")
        print("        - only")

    option = ["relative", "full", "only"]

    if len(sys.argv) != 2 or sys.argv[1] not in option:
        usageMessage()
        exit()


def importDB(*args, **kwargs):
    file_dir_base = "../json/formated/"
    file_dir = []
    file = []
    for arg in args:
        file_dir.append(arg)
    db = []
    for i in range(len(file_dir)):
        f_dir = file_dir_base + file_dir[i]
        file.append(open(f_dir, "r"))
        db_temp = json.load(file[i])
        for data in db_temp:
            db.append(data)
    return db


def importLIB(*args, **kwargs):
    file_dir_base = "../json/library/"
    file_dir = []
    file = []
    for arg in args:
        file_dir.append(arg)
    lib = []
    for i in range(len(file_dir)):
        f_dir = file_dir_base + file_dir[i]
        file.append(open(f_dir, "r"))
        lib_temp = json.load(file[i])
        for data in lib_temp:
            lib.append(data)
    return lib


def get_matchList(*args, **kwargs):
    file_dir_base = "./output_files/"
    file_dir = []
    file = []
    for arg in args:
        file_dir.append(arg)
    match_list = []
    for i in range(len(file_dir)):
        f_dir = file_dir_base + file_dir[i]
        file.append(open(f_dir, "r"))
        match_list_temp = json.load(file[i])
        for data in match_list_temp:
            match_list.append(data)
    return match_list


def optionGetURL(option):
    if option == "relative":
        return option + "_list.json"

    if option == "full":
        return option + "match_list.json"

    if option == "only":
        return option + "match_list.json"

def feedData(song, data):
    dataname = ["lyrics", "album", "lyricist", "composer", "translator"]
    for name in dataname:
        song[name] = data[name]
    return song

def onlyHunter(db, lib, matchList):
    db_len = len(db)
    counter = 0

    for song in db:
        for match_item in matchList:
            if song["sid"] == match_item["sid"]:
                for data in lib:
                    if data["id_"] == match_item["onlymatch_ID"]:
                        song = feedData(song, data)
        counter += 1
        print("Only Hunter: [" + str(counter) + " / " + str(db_len) + " ]")
    
    print("Only Hunter: Mission Completed.")
    return db


def output_to_JSON(newDB, outName):
    outURL = "output_files/" + outName + ".json"
    outFile = open(outURL, "w")
    outFile.write(json.dumps(newDB, ensure_ascii=False))

    print("Wrote new data > \"" + outURL + "\" done.")


if __name__ == "__main__":
    option = sys.argv[1]

    if option != "only":
        exit() # 暫時只開放 option: only

    listURL = optionGetURL(option)
    db = importDB("chinese.json", "taiwanese.json")
    lib = importLIB("songDB_got.json")
    matchList = get_matchList(listURL)
    newDB = onlyHunter(db, lib, matchList)
    output_to_JSON(newDB, "worshipDB")
