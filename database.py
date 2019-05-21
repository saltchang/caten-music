#!/usr/bin/env/ python3
# database.py


import sys

from caten_worship import create_app

def dropAll(config_code):

    app = create_app(config_code)

    from caten_worship.models.base import db

    db.drop_all()


def createAll(config_code):

    app = create_app(config_code)

    from caten_worship.models.base import db

    db.create_all()


def print_usage():

    print()
    print("Usage: database.py [command] [config_code]")
    print()
    print("[command]")
    print()
    print("drop : Drop all tables in the database.")
    print("create : Create all tables into the database.")
    print()
    print("[config_code]")
    print()
    print("default : non-test")
    print("test : test")


if __name__ == "__main__":

    if len(sys.argv) == 3:
        command = sys.argv[1]
        config_code = sys.argv[2]
        if command == "drop":
            if config_code == "test":
                dropAll("test")
            else:
                print_usage()
        elif command == "create":
            if config_code == "test":
                createAll("test")
            else:
                print_usage()
        else:
            print_usage()
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "drop":
            dropAll("")
        elif command == "create":
            createAll("")
        else:
            print_usage()
    else:
        print_usage()
