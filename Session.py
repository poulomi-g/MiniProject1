try:
    import sqlite3
    import os
    from datetime import datetime
    import time


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def startSession(uid, conn, db):

    while True:
        print("Session started")
        print()
        print("********************************")
        print("What would you like to do today?")
        print()
        print("1. Post a question: ")
        print("2. Search for posts")
        print("3. Logout")
        print()
        action = input("Your selection: ")
        print("********************************")

        if int(action) == 3:
            os.system('clear')
            print("Successfully logged out")
            break

    return
