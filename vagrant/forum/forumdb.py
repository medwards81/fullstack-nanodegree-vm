#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    con = psycopg2.connect("dbname=forum")
    cur = con.cursor()
    cur.execute("SELECT time, content FROM posts ORDER BY time DESC")
    rows = cur.fetchall()
    con.close()

    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in rows]
    posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Database connection
    con = psycopg2.connect("dbname=forum")
    cur = con.cursor()

    t = time.strftime('%c', time.localtime())

    cur.execute("INSERT INTO posts VALUES(%s, %s)", (content, t,))
    con.commit()
    con.close()


