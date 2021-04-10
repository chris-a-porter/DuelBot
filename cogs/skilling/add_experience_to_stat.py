import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

# Returns the level after adding experience to it


async def add_experience_to_stat(self, user_id, skill, gained_xp):
    sql = f"""
    UPDATE user_skills
    SET {skill}_xp = {skill}_xp + {gained_xp}
    WHERE user_id = {user_id}
    """

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 36", error)
    finally:
        if conn is not None:
            conn.close()

    after_level = await self.getLevel(user_id, skill)
    return after_level
