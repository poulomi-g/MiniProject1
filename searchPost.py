try:
    import sqlite3
    import os
    from datetime import datetime
    import time


except ImportError as args:
    print("Import Error:", args)
    exit(1)


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
            HAVING ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?))
    """
    # insert query statement for all matchings
    for i in range(len(keywords) - 1):
        query += "OR ((posts.title LIKE ?) OR (posts.body LIKE ?) OR (tags.tag LIKE ?)) \n"

    # append the keywords into input tuple
    queryInputs = []
    for k in keywords:
        kString = "%" + k + "%"
        for i in range(3):
            queryInputs.append(kString)

    queryInputs = tuple(queryInputs)
    result = db.execute(query, queryInputs).fetchall()

    print(result)
