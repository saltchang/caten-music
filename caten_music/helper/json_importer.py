# helper/json_importer.py

# 暫不使用

import json


def importJSON(*args, **kwargs):

    file_dir_base = "data/"
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
