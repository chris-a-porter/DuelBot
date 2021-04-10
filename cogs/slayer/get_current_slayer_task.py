import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def get_current_slayer_task(self, user_id):
    sql = F"""SELECT
    slayer_task,
    slayer_monster_count
    FROM user_skills
    WHERE user_id = {user_id}
    """

    # List element containing the user's slayer experience
    task = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        for row in data:
            task = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 311", error)
    finally:
        if conn is not None:
            conn.close()
    return task


