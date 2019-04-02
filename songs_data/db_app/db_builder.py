import json


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


if __name__ == "__main__":

    db = importDB("chinese.json", "taiwanese.json")
    lib = importLIB("songDB_got.json")

    counter = 0

    matchID = []
    fullmatch_songs = []

    full_match = []
    only_match = []
    db_rebulid = []

    counter = 0
    process_len = len(db)*len(lib)

    for song in db:
        fullmatch_songs = []
        for data in lib:
            if data["title"] == song["title"]:
                fullmatch_songs.append(data["id_"])
        if len(fullmatch_songs) == 1:
            song["lyrics"] = data["lyrics"]
            song["album"] = data["album"]
            song["lyricist"] = data["lyricist"]
            song["composer"] = data["composer"]
            song["translator"] = data["translator"]
        db.append(song)
        counter += 1
        print(" [%.2f " % (100*counter/process_len) + "%] - " + str(counter) + " / " + str(process_len) + " songs finished")

    
    output_DB = open("../json/DB/worshipDB.json", "w")
    output_DB.write(json.dumps(db, ensure_ascii=False))


# Get the match ID
    # for song in db:
    #     fullmatch_songs = []
    #     for data in lib:
    #         if data["title"] == song["title"]:
    #             fullmatch_songs.append(data["id_"])
    #             print(data["title"] + " fully matched to: " + song["title"])
    #     if len(fullmatch_songs) != 0:
    #         full_match.append(
    #             {"title": song["title"], "uid": song["uid"], "matched_data_id": fullmatch_songs})

    #     if len(fullmatch_songs) == 1:
    #         only_match.append({"title": song["title"], "uid": song["uid"]})

    #         if data["title"].find(song["title"]) != -1:
    #             # matchID.append(song["uid"])
    #             # counter += 1
    #             # print(str(counter) + " / " + str(len(db) * len(lib)))
    #             print(data["title"] + " matched to: " + song["title"])

# Write output file
    # full_match_file = open("output_files/full_match.json", "w")
    # full_match_file.write(json.dumps(full_match, ensure_ascii=False))
    # only_match_file = open("output_files/only_match.json", "w")
    # only_match_file.write(json.dumps(only_match, ensure_ascii=False))
