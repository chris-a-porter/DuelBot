import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


async def gp(self, message):
    await self.createTablesForUser(message.author)

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
            commaMoney = "{:,d}".format(row[0])
            await message.send(f'{ItemEmojis.Coins.coins} You have {commaMoney} GP {ItemEmojis.Coins.coins}')

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("GP ERROR", error)
        return
    finally:
        if conn is not None:
            conn.close()