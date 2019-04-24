#!/usr/bin/env/ python3
# database.py


import sys

from caten_worship.models.base import db

from caten_worship import create_app

def dropAll():

    app = create_app

    db.drop_all()


def createAll():

    app = create_app

    db.create_all()


def print_usage():

    print()
    print("Usage: database.py [command]")
    print()
    print("[command]")
    print()
    print("drop : Drop all tables in the database.")
    print("create : Create all tables into the database.")


if __name__ == "__main__":

    command = sys.argv[1]

    if len(sys.argv) == 2:
        if command == "drop":
            dropAll()
        elif command == "create":
            createAll()
        else:
            print_usage()
    else:
        print_usage()
