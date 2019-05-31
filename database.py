#!/usr/bin/env/ python3
# database.py


import sys

from caten_worship import CreateApp

def dropAllMain():

    app = CreateApp.Main()

    from caten_worship.models.base import db

    db.drop_all()

def dropAllTest():

    app = CreateApp.Test()

    from caten_worship.models.base import db

    db.drop_all()


def createAllMain():

    app = CreateApp.Main()

    from caten_worship.models.base import db

    db.create_all()

def createAllTest():

    app = CreateApp.Test()

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
    print("default(null) : non-test")
    print("test : test")


if __name__ == "__main__":

    if len(sys.argv) == 3:
        command = sys.argv[1]
        config_code = sys.argv[2]
        if command == "drop":
            if config_code == "test":
                dropAllTest()
            else:
                print_usage()
        elif command == "create":
            if config_code == "test":
                createAllTest()
            else:
                print_usage()
        else:
            print_usage()
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "drop":
            dropAllMain()
        elif command == "create":
            createAllMain()
        else:
            print_usage()
    else:
        print_usage()
