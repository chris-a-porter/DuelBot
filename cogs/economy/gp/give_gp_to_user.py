import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def give_gp_to_user(message, user_id, amount):

    sql = f"""
    UPDATE duel_users 
    SET gp = gp + {amount} 
    WHERE user_id = {user_id}
    """
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("REMOVING GP ERROR", error)
    finally:
        if conn is not None:
            conn.close()
