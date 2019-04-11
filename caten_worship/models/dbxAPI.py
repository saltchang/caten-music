# models/dbxAPI.py

import dropbox, os

def get_dbx():
    dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN"))
    return dbx