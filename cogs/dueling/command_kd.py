import psycopg2
import discord

async def kd(self, message):
    await self.createTablesForUser(message.author)

    sql = f"""
    SELECT
    nick nick,
    wins wins,
    losses losses

    FROM duel_users
    WHERE user_id = {message.author.id}"""

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute(sql)

        rows = cur.fetchall()

        for row in rows:
            embed = discord.Embed(title=f"K/D for {message.author.id}", color=discord.Color.green())
            embed.add_field(name="**Wins**", value=row[1])
            embed.add_field(name="**Losses**", value=row[2])
            embed.add_field(name="**KDA**", value=round((row[1] / row[2]), 2))

            await message.send(embed=embed)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("KD ERROR", error)
        return
    finally:
        if conn is not None:
            conn.close()
