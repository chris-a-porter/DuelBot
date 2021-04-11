import psycopg2
import os
import time

DATABASE_URL = os.environ['DATABASE_URL']


async def checkTripTime(ctx):
    sql = f"""
    SELECT
    finishtime
    FROM user_skills
    WHERE user_id = {ctx.author.id}
    """

    conn = None
    activity_info = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            activity_info = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 90", error)
    finally:
        if conn is not None:
            conn.close()
    if row[0] is None:
        return time.time()
    else:
        return row[0]