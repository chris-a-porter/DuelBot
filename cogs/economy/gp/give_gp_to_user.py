import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def give_gp_to_user(message, amount):

    sql = f"""
    INSERT INTO user_items (user_id, item_id, quantity) VALUES ({message.author.id}, 995, {amount})
    ON CONFLICT (user_id, item_id) DO UPDATE SET quantity = user_items.quantity + EXCLUDED.quantity
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
