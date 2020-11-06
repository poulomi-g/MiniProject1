try:
    import sqlite3
    import os
    from datetime import datetime
    import time
    from postActions import *


except ImportError as args:
    print("Import Error:", args)
    exit(1)


def showResults(uid, result, conn, db):
    if len(result) < 5:
        for i in range(len(result)):
            print(result[i])
        print("View more/actions")
        postActionSelector(uid, result, 5, conn, db)

    else:
        for i in range(5):
            print(result[i])
        print("View more/actions")
        postActionSelector(uid, result, len(result), conn, db)


def searchPost(uid, conn, db):
    print("SEARCH POSTS")
    print("********************************")
    keywords = input(
        "Enter one or more search keywords: ").lower().split()

    keywords = tuple(keywords)

    # search for supplied keyword
    query = """
        SELECT 
            posts.*,
            IFNULL(COUNT(DISTINCT votes.vno), 0) vcnt,
            CASE
                WHEN posts.pid = questions.pid THEN
                    COUNT(DISTINCT answers.pid)
                ELSE
                    "N/A"
                END countanswers
            FROM posts LEFT JOIN answers ON posts.pid = answers.qid
            LEFT JOIN questions ON questions.pid = posts.pid
            LEFT JOIN votes ON votes.pid = posts.pid
            LEFT JOIN tags ON tags.pid = posts.pid
            GROUP BY posts.pid
    """
    # insert query statement for all matchings
    for i in range(len(keywords)):
        if i == 0:
            query += "HAVING ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?))"
        else:
            query += "OR ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?)) \n"

    # append the keywords into input tuple

    # Order by the number of their apperance, counting only once per keyword
    # since the LIKE keyword will return 1 if match or 0 if not, adding them together return no. of keyword matched

    query += "ORDER BY ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?)) \n"
    for j in range(len(keywords) - 1):
        query += " + ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?)) \n"
    query += "DESC \n"

    # append the keywords into input tuple
    queryInputs = []
    for k in keywords:
        kString = "%" + k + "%"
        for i in range(6):
            queryInputs.append(kString)

    queryInputs = tuple(queryInputs)
    result = db.execute(query, queryInputs).fetchall()

    if not result:
        os.system('clear')
        print("No matching posts")

    else:
        showResults(uid, result, conn, db)
