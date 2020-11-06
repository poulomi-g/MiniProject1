try:
    import sqlite3
    import os
    from datetime import datetime
    import time
    from creatQuestionPost import pidAssign


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def showResults(uid, result, conn, db):
    if len(result) < 5:
        for i in range(len(result)):
            print(result[i])

    else:
        for i in range(5):
            print(result[i])
        print("View more/actions")
        postActionSelector(uid, result, 5, conn, db)


def displayMore(uid, result, start, conn, db):
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


def answerPost(user, conn, db):
    print()
    post = input("Which post would you like to answer: ")

    # Check if post exists:
    posts = db.execute(
        "SELECT pid FROM questions WHERE questions.pid = ? ", (post,)).fetchall()

    # If no such posts:
    if not posts:
        return False

    else:
        answer_qid = posts[0][0]

        post_title = input("Enter your post title: ")
        post_body = input("Enter your post body: ")

        # Enter null check here

        print("Posting")

        try:
            answer_pid = pidAssign(conn, db)
            post_date = datetime.date(datetime.now())
            db.execute("INSERT INTO posts (pid, pdate, title, body, poster) VALUES (?,?,?,?,?)",
                       (answer_pid, post_date, post_title, post_body, user))
            conn.commit()

            db.execute("INSERT INTO answers (pid, qid) VALUES (?, ?)",
                       (answer_pid, answer_qid))
            conn.commit()
            return conn, db

        except:
            print("No more post space")
            return False


def postActionSelector(uid, result, end, conn, db):
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
            end = displayMore(uid, result, end, conn, db)
            continue

        if int(action) == 1:
            status = answerPost(uid, conn, db)

            if not status:
                os.system('clear')
                print("No such posts!")

            else:
                os.system('clear')
                conn, db = status
                print("Post created!")

            return conn, db
