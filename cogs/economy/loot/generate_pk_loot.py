from cogs.economy.roll_random_loot import roll_random_loot
import psycopg2
import os
import discord
from cogs.item_files.emojis_list import misc_items

DATABASE_URL = os.environ['DATABASE_URL']


async def generate_pk_loot(message):
    lastmsg = await message.send('*Checking the loot pile...*')
    loot = await roll_random_loot(message, 3, 6, 0)

    sql = f"""
    UPDATE duel_users 
    SET gp = gp + {loot[995][1]} 
    WHERE user_id = {message.author.id}
    """
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 3", error)
    finally:
        if conn is not None:
            conn.close()

        loot_message = ""

        for item in loot.values():
            if item[0] != 'Coins':

                each = ''

                if item[3] > 1 and type(item[2]) != int:
                    each = ' each'

                loot_message += f"*{item[3]}x {item[4]} {item[0]} worth {item[2]} GP{each}* \n"

        comma_money = "{:,d}".format(loot[995][1])
        loot_message += f"Total loot value: **{comma_money} GP** {misc_items['coins']}"

        embed = discord.Embed(title=f"**{message.author.nick} received some loot from their kill:**",
                              color=discord.Color.dark_teal())
        embed.add_field(name="Loot", value=loot_message)
        await lastmsg.edit(embed=embed)
