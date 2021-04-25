import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def get_current_slayer_master(user_id):
    sql = F"""SELECT
       slayer_master
       FROM user_skills
       WHERE user_id = {user_id}
       """
    # List element containing the user's slayer experience
    master = None

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
        print("SOME ERROR 34567", error)
    finally:
        if conn is not None:
            conn.close()

    master = row[0]
    return master
