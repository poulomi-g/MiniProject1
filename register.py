try:
    import sqlite3
    import os

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def register(conn, db):
    os.system('clear')

    userFlag
    while True:
        print('REGISTRATION')
        print("********************************")
        print()
        new_uid = input("New user ID (Make sure it's unique!): ")
        new_name = input("Name: ")
        new_city = input("City: ")
        new_pwd = input("Enter password: ")
        new_pwd_confirm = input("Re-enter password: ")

        print()
        print("********************************")

        # UID checks:
        userFlag = 0

        # UID must be non-null:
        if not new_uid:
            os.system('clear')
            print("ERROR: User ID must be non-null! Try again")
            continue

        # UID must be unique:
        existing_users = db.execute(
            "SELECT users.uid FROM users WHERE LOWER(users.uid) = LOWER(?)", (new_uid, )).fetchall()

        if not existing_users:
            userFlag = 1

        else:
            os.system('clear')
            print('Username not unique!')
            continue
