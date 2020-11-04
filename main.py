try:
    import sys
    import os
    import os.path
    import sqlite3
    # from getpass import getpass
    # from datetime import datetime
    # import time
    # import SystemFunctions
except ImportError as args:
    print("Import Error:", args)
    exit(1)


def main():
    try:
        # Check if db file is included in main.py call
        if len(sys.argv) != 2:
            print("Not enough arguments!")
            exit(0)
        # Check if valid db file by comparing last 3 letters
        elif sys.argv[1][len(sys.argv[1]) - 3:] != ".db":
            print("Not a database (.db) file!")
            exit(0)

        path = sys.argv[1]
        conn = sqlite3.connect(path)
        os.system('clear')
        print("Connection successful!")

    except:
        print("Input error, exiting...")

    db = conn.cursor()

    # Menu action will run every time there input error
    while True:
        print("********************************")
        print()
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print()
        print("********************************")
        print()
        action = input("Choose from one of the above: ")

        try:
            action = int(action)
        except:
            os.system('clear')
            print("Input could not be casted to integer. Please enter digit")
            continue

        # If input integer:

        if action == 1:
            register(conn, db)

        elif action == 2:
            login(conn, db)

        elif action == 3:
            print("Exiting...")
            exit(0)

        else:
            os.system('clear')
            print("Input not available!")
            continue


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print()
        print("Exiting...")
        exit(0)
