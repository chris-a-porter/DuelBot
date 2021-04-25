import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def get_slayer_points(ctx):
    sql = f"""
    SELECT
    slayer_points
    FROM user_skills
    WHERE user_id = {ctx.author.id}
    """

    points = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        for row in data:
            points = row[0]
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 34567", error)
    finally:
        if conn is not None:
            conn.close()
        return points
