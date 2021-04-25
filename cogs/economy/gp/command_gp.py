import os
import psycopg2
from cogs.item_files.emojis_list import misc_items

DATABASE_URL = os.environ['DATABASE_URL']
# Retrieve the amount of GP a user has and send it to the channel they requested it from


async def gp(message):

    sql = f"""
    SELECT
    gp gp
    FROM duel_users
    WHERE user_id = {message.author.id}
    """

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            comma_money = "{:,d}".format(row[0])
            await message.send(f'{misc_items["coins"]} You have {comma_money} GP.')

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("GP ERROR", error)
        return
    finally:
        if conn is not None:
            conn.close()
