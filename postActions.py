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
    if len(result) - start < 5:
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


def votePost(user, conn, db):
    print()
    post = input("Which post would you like to vote: ")

    # Check if post exists:
    posts = db.execute(
        "SELECT pid FROM posts WHERE posts.pid = ? ", (post,)).fetchall()

    # If no such posts:
    if not posts:
        print(1)
        return False

    else:
        # Check if post already has a vote from user:
        existing_vote = db.execute(
            "SELECT votes.vno FROM votes WHERE votes.uid = ? AND votes.pid = ?", (user, posts[0][0],))

        if not existing_vote:
            vote_date = datetime.date(datetime.now())
            vote_uid = user
            vote_pid = posts[0][0]

            # Assign vno:
            # Check if table empty:
            emptyCheck = db.execute("SELECT * from votes").fetchall()
            vno = 0
            if not emptyCheck:
                # No votes yet
                vno = 1

            else:
                maxvote = db.execute("SELECT COUNT(vno) FROM votes").fetchall()
                if int(maxvote[0][0]) < 9999:
                    vno += 1
                else:
                    print("Max total votes")
                    return False

            db.execute("INSERT INTO votes (pid, vno, vdate, uid) VALUES(?, ?, ?, ?)",
                       (vote_pid, vno, vote_date, user))
            conn.commit()
            return True

        else:
            print("This post has already been voted by you")
            return False


def checkPriviledge(user, conn, db):
    # check if user is a privileged user
    user = user.lower()
    privileged_user = False
    rows = db.execute("SELECT uid FROM privileged")
    rows = db.fetchall()
    if not rows:
        print("No privileged users yet")
        return False
    else:
        try:
            for elem in rows:
                if elem[0].lower() == user:
                    priveleged_user = True
                    return priveleged_user
        except:
            return False


def acceptAnswer(uid, conn, db):
    # Check if post exists in answers:
    print()
    post = input("Which post would you like to mark as accepted answer: ")

    # Check if post exists:
    existingAnswer = db.execute(
        "SELECT * FROM answers WHERE answers.pid = ? ", (post,)).fetchall()

    if not existingAnswer:
        print("Answer post doesnt exist, try again")
        return False

    else:
        # Check if question has an answer already:
        question_pid = existingAnswer[0][1]
        answer_pid = existingAnswer[0][0]
        print(question_pid)
        print(answer_pid)

        matchingQuestion_theaid = db.execute(
            "SELECT IFNULL(questions.theaid, 0) FROM questions WHERE questions.pid = ?", (question_pid,)).fetchall()

        print(matchingQuestion_theaid)
        if matchingQuestion_theaid[0][0] == 0:  # No assigned answer yet
            db.execute("UPDATE questions SET theaid = ? WHERE pid = ?",
                       (answer_pid, question_pid,))
            conn.commit()
            print("Worked")
            return True

        else:
            action = input(
                "This post already has an assigned answer. Would you like to change it? (y/n): ")

            if action == 'n':
                return False

            else:
                db.execute("UPDATE questions SET theaid = ? WHERE pid = ?",
                           (answer_pid, question_pid,))
                conn.commit()
                print("Worked")
                return True


def convertTuple(tup):
    str = ''.join(tup)
    return str


def check_badge(badgename, cursor):  # checks if badge name is valid
    badgeList = [badgename.lower()]
    cursor.execute(
        "SELECT bname from badges WHERE lower(bname) = ?;", badgeList)
    if cursor.fetchone():
        return True
    else:
        return False


def give_badge(user, conn, cursor):
    print()
    pid = input("Which post would you like to give a badge to: ")

    # Check if post exists:
    posts = cursor.execute(
        "SELECT pid FROM posts WHERE posts.pid = ? ", (pid,)).fetchall()

    if not posts:
        print("No such posts exists")
        return False

    badge_name = input("please input the badge name you would like to give: ")
    badge_condition = True
    while badge_condition:
        if check_badge(badge_name, cursor) == True:
            badge_condition = False
        else:
            badge_name = input(
                "you inputted an incorrect badge name, please try again: ")
            continue

    checkList = [pid.lower()]
    cursor.execute(
        " SELECT poster from posts WHERE lower(pid) = ?;", checkList)
    poster = cursor.fetchone()
    poster = convertTuple(poster)
    checkList = [poster.lower(), badge_name.lower()]
    cursor.execute(
        " INSERT OR REPLACE INTO ubadges (uid, bdate, bname) VALUES (?, date('now'), ?); ", checkList)
    conn.commit()
    print("badge succesfully added")


def postActionSelector(uid, result, end, conn, db):
    while True:
        print("What would you like to do next: ")
        print("0. Go back")
        print("1. Answer a post")
        print("2. Vote a post")
        if end != None:
            print("3. View next page of results: ")
        print()
        if checkPriviledge(uid, conn, db):
            print("4. Mark answer as accepted")
            print("5. Give a badge")
            print("6. Add a tag")
            print("7. Update a post")

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
                continue

            else:
                os.system('clear')
                conn, db = status
                print("Post created!")
                break

        if int(action) == 2:
            # os.system('clear')
            voteStatus = votePost(uid, conn, db)

            if voteStatus:
                print("Vote successful")
                break

            else:
                print("Try again")
                continue

        if int(action) == 4:
            acceptAnswerStatus = acceptAnswer(uid, conn, db)

            if acceptAnswerStatus:
                os.system('clear')
                print("Marked as accepted")
                break

            else:
                os.system('clear')
                print('No answer marked as accepted')
                continue

        if int(action) == 5:
            badgeStatus = give_badge(uid, conn, db)

    return conn, db
