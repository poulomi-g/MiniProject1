try:
    import sqlite3
    import os
    from datetime import datetime
    import time

except ImportError as args:
    print("Import Error:", args)
    exit(1)


def register(conn, db):
    os.system('clear')

    userFlag = 0
    pwdFlag = 0
    crdate = datetime.date(datetime.now())
    while True:
        print('REGISTRATION')
        print("********************************")
        print()
        new_uid = input("New user ID (Make sure it's unique!): ")

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
            print('ERROR: Username not unique! Try again')
            continue

        new_name = input("Name: ")
        new_city = input("City: ")
        new_pwd = input("Enter password: ")
        new_pwd_confirm = input("Re-enter password: ")

        # Password checks

        # Non-null
        if (not new_pwd or not new_pwd_confirm):
            os.system('clear')
            print("ERROR: Password cannot be null. Try again")
            continue

        elif (new_pwd != new_pwd_confirm):
            os.system('clear')
            print("ERROR: Passwords dont match")

        else:
            pwdFlag = 1

        print()
        print("********************************")

        # If uid and
        if (userFlag == 1 and pwdFlag == 1):
            db.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                       (new_uid, new_name, new_pwd, new_city, crdate))
            conn.commit()
            os.system('clear')
            print("The following user has been entered into the database: ")
            print(new_uid)
            print("Returning to main menu...")
            time.sleep(2)
            break
