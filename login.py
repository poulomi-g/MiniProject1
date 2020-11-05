try:
    import sqlite3
    import os
    from datetime import datetime
    import time
    from Session import startSession

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def login(conn, db):
    os.system('clear')

    while True:
        print('LOGIN')
        print("********************************")
        print()
        login_uid = input("User ID: ")

        # Check if null:
        if not login_uid:
            os.system('clear')
            print("ERROR: No username entered. Try again")
            continue

        # Check if username exists in database
        existing_usernames = db.execute(
            "SELECT users.uid FROM users WHERE lower(uid) = lower(?)", (login_uid,)).fetchall()

        if not existing_usernames:
            os.system('clear')
            print("ERROR: Username does not exist in database. Try again")
            continue

        login_pwd = input("Password: ")

        # Checking password entered is null
        if not login_pwd:
            os.system('clear')
            print("ERROR: No password entered. Try again")
            continue

        # Checking if username + password pair exists in database

        credentials = db.execute(
            "SELECT users.uid FROM users WHERE lower(uid) = lower(?) AND pwd = ?", (login_uid, login_pwd)).fetchall()

        if not credentials:
            os.system('clear')
            print('ERROR: Wrong password. Try again')
            continue

        else:
            os.system('clear')
            print("The following user is now logged in: ")
            user = credentials[0][0]
            print(user)
            print()
            print("Starting session...")
            startSession(user, conn, db)
            return
