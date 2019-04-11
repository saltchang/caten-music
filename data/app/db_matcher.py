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


def get_relative_list(db, lib):
    counter = 0
    len_db = len(db)
    len_lib = len(lib)

    relative_list = []
    for song in db:
        song_ = {"uid": song["uid"], "relative_ID": []}
        for data in lib:
            if data["title"].find(song["title"]) != -1:
                song_["relative_ID"].append(data["id_"])
        relative_list.append(song_)
        counter += 1
        print("Get Relative List: [ " +
              str(counter) + " / " + str(len_db) + " ]")

    return relative_list


def get_fullmatch_list(db, lib):
    counter = 0
    len_db = len(db)
    len_lib = len(lib)

    fullmatch_list = []
    for song in db:
        song_ = {"uid": song["uid"], "fullmatch_ID": []}
        for data in lib:
            if data["title"] == song["title"]:
                song_["fullmatch_ID"].append(data["id_"])
        fullmatch_list.append(song_)
        counter += 1
        print("Get Full Match List: [ " +
              str(counter) + " / " + str(len_db) + " ]")

    return fullmatch_list


def get_onlymatch_list(db, lib):
    counter = 0
    len_db = len(db)
    len_lib = len(lib)

    onlymatch_list = []

    for song in db:
        song_ = {"uid": song["uid"], "onlymatch_ID": ""}
        fullmatch_list = []
        for data in lib:
            if data["title"] == song["title"]:
                fullmatch_list.append(data["id_"])
        if len(fullmatch_list) == 1:
            song_["onlymatch_ID"] = fullmatch_list[0]
            onlymatch_list.append(song_)
        counter += 1
        print("Get Only Match List: [ " +
              str(counter) + " / " + str(len_db) + " ]")

    return onlymatch_list


def listFile_output_to_JSON(list, outName):
    outURL = "output_files/" + outName + ".json"
    outFile = open(outURL, "w")
    outFile.write(json.dumps(list, ensure_ascii=False))

    print("Wrote list data > \"" + outURL + "\" done.")


if __name__ == "__main__":
    argsCheck()

    db = importDB("chinese.json", "taiwanese.json")
    lib = importLIB("songDB_got.json")

    option = sys.argv[1]

    if option == "relative":
        relative_list = get_relative_list(db, lib)
        listFile_output_to_JSON(relative_list, "relative_list")

    if option == "full":
        fullmatch_list = get_fullmatch_list(db, lib)
        listFile_output_to_JSON(fullmatch_list, "fullmatch_list")

    if option == "only":
        onlymatch_list = get_onlymatch_list(db, lib)
        listFile_output_to_JSON(onlymatch_list, "onlymatch_list")
