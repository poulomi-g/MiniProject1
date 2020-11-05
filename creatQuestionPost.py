try:
    import sqlite3
    import os
    from datetime import datetime
    import time


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def pidAssign(conn, db):
    # Most recent pid will have maximum value:
    latest_entry = db.execute("SELECT MAX(pid) from posts").fetchall()

    if not latest_entry[0][0]:
        return 'p100'

    else:
        latest_entry_num = int(latest_entry[0][0][1:])
        return 'p' + str(latest_entry_num + 1)


def createQuestionPost(uid, conn, db):
    while True:
        print("CREATE QUESTION")
        print("********************************")

        post_title = input("Enter your post title: ")
        post_body = input("Enter your post body: ")

        # Add checks for posts here

        post_date = datetime.date(datetime.now())
        post_uid = uid

        # Assign post ID:
        ## Format: pXXX
        post_id = pidAssign(conn, db)
        try:
            db.execute("INSERT INTO posts (pid,pdate,title,body,poster) VALUES (?,?,?,?,?)",
                       (post_id, post_date, post_title, post_body, post_uid))
            conn.commit()
            db.execute(
                "INSERT INTO questions (pid, theaid) VALUES (?, NULL)", (post_id, ))
            conn.commit()
            os.system('clear')
            print("Post created!")
            break
        except:
            os.system('clear')
            print("ERROR: Something went wrong, try again")
            continue
