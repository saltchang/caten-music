import json

def importDB():
    file_dir_base = "./songs_data/new/"
    file_dir = ["songs_chinese_new.json", "songs_taiwanese_new.json"]
    file = []
    db = []
    for i in range(len(file_dir)):
        f_dir = file_dir_base + file_dir[i]
        file.append(open(f_dir, "r"))
        db_temp = json.load(file[i])
        for data in db_temp:
            db.append(data)
    return db
