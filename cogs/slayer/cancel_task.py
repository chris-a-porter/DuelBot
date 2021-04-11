import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def cancel_task(self, ctx):
    sql = f"""
    UPDATE user_skills
    SET slayer_task = 0, slayer_monster_count = 0, currently_slaying = false, slayer_points = slayer_points - 30
    WHERE user_id = {ctx.author.id}
    """

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 1923", error)
        return
    finally:
        if conn is not None:
            conn.close()
        await ctx.send("You have cancelled your slayer task. Type `=slay task` to get a new one")
        return
