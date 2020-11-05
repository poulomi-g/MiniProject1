try:
    import sqlite3
    import os
    from datetime import datetime
    import time
    from creatQuestionPost import createQuestionPost
    from searchPost import searchPost


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def startSession(uid, conn, db):
    print("Session started")

    while True:

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

        if not action:
            os.system('clear')
            print("ERROR: Please select an action")
            continue

        if not action.isdigit():
            os.system('clear')
            print("ERROR: Please enter one of the given options")
            continue

        if int(action) == 3:
            os.system('clear')
            print("Successfully logged out")
            break

        elif int(action) == 1:
            os.system('clear')
            createQuestionPost(uid, conn, db)

        elif int(action) == 2:
            os.system('clear')
            searchPost(uid, conn, db)

    return
