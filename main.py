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

        print("Connection successful!")

    except:
        print("Error, exiting...")


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)