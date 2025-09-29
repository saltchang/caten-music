# models/dbx.py

import os

import dropbox


def get_dbx():
    dbx = dropbox.Dropbox(os.environ.get('DROPBOX_ACCESS_TOKEN'))
    # dbx = dropbox.Dropbox(os.environ.get("DROPBOX_ACCESS_TOKEN_CATEN"))
    return dbx
