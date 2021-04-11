import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def check_if_currently_slaying(ctx):
    sql = f"""
    SELECT
    currently_slaying
    FROM user_skills
    WHERE user_id = {ctx.author.id}
    """

    status = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            status = item[0]
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 9001", error)
    finally:
        if conn is not None:
            conn.close()
        return status
