import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

async def check_user_gp(self, user_id):
    sql = f"""
    SELECT
     gp gp
    FROM duel_users
    where user_id = {user_id}
    """

    conn = None
    user_gp = 0

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            user_gp = row[0]
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("READING GP ERROR", error)
        return
    finally:
        if conn is not None:
            conn.close()
        print(f'user has {user_gp} GP')
        return user_gp
