
  
import sqlite3
import time
import re
import getpass
import sys
from random import randint
from os.path import isfile, getsize

conn = None
cursor = None


def connecting_database(dbname):  # init db cursor
    global conn, cursor
    conn = sqlite3.connect(dbname)
    conn.row_factory = lambda cursor, row: row
    cursor = conn.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return True



def convertTuple(tup):
    str = ''.join(tup)
    return str






def sign_in(userid, passw): 


def specific_menu(user, pid):






def check_privileged(user):  # check if user is a privileged user
    user = user.lower()
    privileged_user = False
    rows = cursor.execute("SELECT uid FROM privileged")
    rows = cursor.fetchall()
    for elem in rows:
        if elem[0].lower() == user:
            priveleged_user = True
            return priveleged_user
    return privileged_user


def question_addition(user):  # U query 1 '1. Post a question'
    p_string = 'p'
    post_title = input("Enter your post title: ")
    post_body = input("Enter your post body: ")
    new_id = randint(200,999)
    new_id = p_string + str(new_id)
    new_id = new_id.lower()
    verifyexist = [new_id]
    cursor.execute(" SELECT pid from posts WHERE lower(pid) = ?; ", verifyexist)
    if cursor.fetchone():
        new_id = randint(200,999)
        new_id = p_string + str(new_id)
    else:
        pass
    cursor.execute('SELECT uid FROM users WHERE lower(uid) = ?', (user.lower(),))
    proper_uid = cursor.fetchone()  # actual uid to enforce foreign key constraints
    postList = [new_id, post_title, post_body, proper_uid[0]]
    cursor.execute(" INSERT INTO posts (pid,pdate, title, body, poster) VALUES (?,date('now'), ?,?,?); ",postList)
    conn.commit()
    questionList = [new_id]
    cursor.execute("INSERT INTO questions (pid) VALUES (?)", questionList)
    conn.commit()
    print("post successfully added")
    main_menu(user)


def search_posts(user):  # U query 2 '2. Search for posts'




def print_results(data, user):  # handle printing search results here
    print(len(data), "result(s) found.")  # prints # of results found
    for i in range(0, len(data), 5):  # iterates 5 at a time, printing results
        print_table(data[i:i + 5])
        valid_input = True
        if len(data[i:i + 5]) == 5 and (i != len(data) - 5):
            user_input = input("Press enter to see next page or enter pid for post actions (press 0 to return to main menu): ")
        else:
            user_input = input("Enter pid for post actions (press 0 to return to main menu): ")
        while valid_input:  # while loop checks if user enters valid inputs
            if re.match('[a-zA-Z]{1}\d{3}', user_input):  # if user enters a pid, call specific_menu(user, pid)
                if check_pid(user_input):
                    valid_input = False
                    specific_menu(user, user_input)
                    main_menu(user)
                else:
                    print("Invalid Input. Please try again.")
                    user_input = input(
                        "Press enter to see next page or enter pid for post actions (press 0 to return to main menu): ")
            elif user_input == '':  # if users presses enter, show next page of results
                if len(data[i:i + 5]) != 5 or (i == len(data) - 5):
                    user_input = input("Enter pid for post actions (press 0 to return to main menu): ")
                else:
                    valid_input = False
                    continue
            elif user_input == '0':  # pressing 0 takes user back to main menu
                valid_input = False
                main_menu(user)
            else:
                print("Invalid Input. Please try again.")
                user_input = input("Press enter to see next page or enter pid for post actions (press 0 to return to main menu): ")


def check_pid(pid):  # checks if pid exists in database; returns bool
    cursor.execute("SELECT pid from posts WHERE lower(pid) = ?;", (pid.lower(),))
    pid = cursor.fetchone()
    if pid is None:
        return False
    else:
        return True


def print_table(data):  # handle printing the table here
    table = PrettyTable(['PID', 'Post Date', 'Title', 'Body', 'Poster', 'Votes', 'Answers'])
    for i in data:  # prints data in table format (prints all results)
        cursor.execute('SELECT count(pid) FROM votes WHERE pid=?', (i[0],))  # gets number of votes
        i = i + cursor.fetchone()
        cursor.execute('SELECT count(qid) FROM answers WHERE qid =?', (i[0],))  # gets number of answers if question
        i = i + cursor.fetchone()
        table.add_row(i)
    print(table)


def add_answer(user, qpost):  # U query 3 '3. Post action-Answer'
    cursor.execute('SELECT pid FROM questions WHERE lower(pid) = ?', (qpost.lower(),))
    qpost = cursor.fetchone()
    if qpost is None:
        print("You must select a question")
        return
    post_title = input("Enter your post title: ")
    post_body = input("Enter your post body: ")
    new_id = randint(200,999)
    new_id = 'p' + str(new_id)
    verifyexist = [new_id.lower()]
    cursor.execute(" SELECT pid from posts WHERE lower(pid) = ?; ", verifyexist)
    if cursor.fetchone():
        new_id = randint(200,999)
        new_id = 'p' + str(new_id)
    else:
        pass
    cursor.execute('SELECT uid FROM users WHERE lower(uid) = ?', (user.lower(),))
    proper_uid = cursor.fetchone()  # actual uid to enforce foreign key constraints
    postList = [new_id, post_title, post_body, proper_uid[0]]
    cursor.execute(" INSERT INTO posts (pid, pdate, title, body, poster) VALUES (?,date('now'), ?,?,?); ", postList)
    conn.commit()
    answerList = [new_id.lower(), qpost[0]]
    cursor.execute("INSERT INTO answers (pid, qid) VALUES (?,?)", answerList)
    conn.commit()
    print("Answer successfully added")


def add_vote(user, pid):  # U query 4 '4. Post action-Vote'
    cursor.execute('SELECT count(pid) FROM votes WHERE lower(pid) = ?', (pid.lower(),))  # gets number of votes
    votes = cursor.fetchone()
    cursor.execute('SELECT pid FROM posts WHERE lower(pid) = ?', (pid.lower(),))
    match_pid = cursor.fetchone()  # actual pid to enforce foreign key constraints
    cursor.execute('SELECT uid FROM users WHERE lower(uid) = ?', (user.lower(),))
    proper_uid = cursor.fetchone()  # actual uid to enforce foreign key constraints
    vno = votes[0] + 1
    vote_list = [match_pid[0], vno, proper_uid[0]]
    cursor.execute(" INSERT INTO votes (pid, vno, vdate, uid) VALUES (?,?,date('now'),?); ", vote_list)
    conn.commit()
    print("Vote successfully added")


def check_badge(badgename):  # checks if badge name is valid
    badgeList = [badgename.lower()]
    cursor.execute("SELECT bname from badges WHERE lower(bname) = ?;", badgeList)
    if cursor.fetchone():
        return True
    else:
        return False


def mark_as_accepted(user, aid):  # PU query 1 '1. Post action-Mark as the accepted'



def give_badge(user, pid):  # PU query 2 '2. Post action-Give a badge'
    privileged_user = check_privileged(user)
    if privileged_user == False:
        print("You are not allowed to use this function\n")
        return

    badge_name = input("please input the badge name you would like to give: ")
    badge_condition = True
    while badge_condition:
        if check_badge(badge_name) == True:
            badge_condition = False
        else:
            badge_name = input("you inputted an incorrect badge name, please try again: ")
            continue

    checkList = [pid.lower()]
    cursor.execute(" SELECT poster from posts WHERE lower(pid) = ?;", checkList)
    poster = cursor.fetchone()
    poster = convertTuple(poster)
    checkList = [poster.lower(), badge_name.lower()]
    cursor.execute(" INSERT OR REPLACE INTO ubadges (uid, bdate, bname) VALUES (?, date('now'), ?); ",checkList)
    conn.commit()
    print("badge succesfully added")


def add_tag(user, pid):  # PU query 3 '3. Post action-Add a tag'
    privileged_user = check_privileged(user)
    if not privileged_user:
        print("You are not allowed to use this function\n")

    else:  # add their tag to table
        #check that tag does not already exist
        tag_duplicate = True;
        new_tag = input("Type the tag you would like to add: ")
        while tag_duplicate:
            rows = cursor.execute("SELECT tag FROM tags")
            rows = cursor.fetchall()
            tag_duplicate = False
            for elem in rows:
                if elem[0].lower() == new_tag.lower():
                    tag_duplicate = True
                    new_tag = input("That tag already exists, try adding different one: ")
        tagList = [pid.lower(), new_tag.lower()]
        cursor.execute("INSERT INTO tags VALUES (?, ?);", tagList)
        conn.commit()
        print("Tag added successfully\n")


def edit_post(user, pid):  # PU query 4 '4. Post Action-Edit'
    privileged_user = check_privileged(user)
    if not privileged_user:
        print("You are not allowed to use this function\n")

    else:  # change title and/or body of post
        edit_condition1 = True
        while edit_condition1:
            user_choice = input("Would you like to edit the title of this post? (Y) or (N) ")
            if user_choice.upper() == 'Y':
                new_title = input("What would you like the new title to be? ")
                titleList = [new_title, pid.lower()]
                cursor.execute(""" UPDATE posts 
                        SET title = ?
                        WHERE pid = ? ;""", titleList)
                conn.commit()
                print("Title changed successfully\n")
                edit_condition1 = False
            elif user_choice.upper() == 'N':
                edit_condition1 = False
            else:
                print("wrong input try again")
                continue
        edit_condition2 = True
        while edit_condition2:
            user_choice = input("Would you like to edit the body of this post? (Y) or (N) ")
            if user_choice.upper() == 'Y':
                new_body = input("What would you like the new body to be? ")
                bodyList = [new_body, pid.lower()]
                cursor.execute(""" UPDATE posts 
                        SET body = ?
                        WHERE pid = ? ;""", bodyList)
                conn.commit()
                print("Body changed successfully\n")
                edit_condition2 = False
            elif user_choice.upper() == 'N':
                edit_condition2 = False
            else:
                print("wrong input try again")

def main():
    exit_condition = True
    # dbname = input("Enter your sqlite database path to continue: ")  # DELETE BEFORE SUBMISSION

    try:
        dbname = sys.argv[1]  # Handles command line sys arguments (can pass db in terminal)
    except:
        print("Missing database file")
        quit()

    while exit_condition:
        connectCheck = connecting_database(dbname)
        if connectCheck:
            print("Database connected succesfully!")
            exit_condition = False
        else:
            print("Database could not be opened.")
            quit()

    login_menu()


if __name__ == "__main__":
    main()


