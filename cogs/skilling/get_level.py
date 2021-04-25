import psycopg2
import os
from helpers.xp_to_level import xp_to_level

DATABASE_URL = os.environ['DATABASE_URL']


async def get_level(user_id, skill):
    sql = F"""SELECT
    {skill}_xp
    FROM user_skills
    WHERE user_id = {user_id}
    """

    # List element containing the user's slayer experience
    level = 1
    row = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        for row in data:
            data = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 3", error)
    finally:
        if conn is not None:
            conn.close()

    level = xp_to_level(row[0])
    return level
