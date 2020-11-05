try:
    import sqlite3
    import os
    from datetime import datetime
    import time

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def startSession(uid, conn, db):
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
