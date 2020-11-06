try:
    import sqlite3
    import os
    from datetime import datetime
    import time


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def displayMore(result, start, conn, db):
    print(start)
    print(len(result))
    if (start) < len(result):
        for i in range(start, len(result)):
            print(result[i])
        print("End of results")
        return None  # No more results left

    else:
        for i in range(start, start+5):
            print(result[i])
        return start+5


def postActionSelector(result, end, conn, db):
    while True:
        print("What would you like to do next: ")
        print("0. Go back")
        print("1. Answer a post")
        print("2. Vote a post")
        if end != None:
            print("3. View next page of results: ")
        print()
        action = input("Your action: ")

        if int(action) == 0:
            print("Going back...")
            break

        if int(action) == 3:
            end = displayMore(result, end, conn, db)
            continue
