import discord
import psycopg2
import os
from cogs.item_files.emojis_list import rares

DATABASE_URL = os.environ['DATABASE_URL']


async def command_rares(message):

    cmds = f"""
    SELECT
        _1038 red_partyhat,
        _1040 yellow_partyhat,
        _1042 blue_partyhat,
        _1044 green_partyhat,
        _1046 purple_partyhat,
        _1048 white_partyhat,
        _962 christmas_cracker,
        _1057 red_hween_mask,
        _1055 blue_hween_mask,
        _1053 green_hween_mask,
        _1050 santa_hat,
        _1959 pumpkin,
        _1961 easter_egg

    FROM duel_rares
    WHERE user_id = {message.author.id}"""

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(cmds)

        rows = cur.fetchall()

        for row in rows:
            embed = discord.Embed(title=f"{message.author.id}'s rares", color=discord.Color.blurple())
            embed.add_field(name=f"**Red partyhat** {rares['red_partyhat']}", value=row[0])
            embed.add_field(name=f"**Yellow partyhat** {rares['yellow_partyhat']}", value=row[1])
            embed.add_field(name=f"**Blue partyhat** {rares['blue_partyhat']}", value=row[2])
            embed.add_field(name=f"**Green partyhat** {rares['green_partyhat']}", value=row[3])
            embed.add_field(name=f"**Purple partyhat** {rares['purple_partyhat']}", value=row[4])
            embed.add_field(name=f"**White partyhat** {rares['white_partyhat']}", value=row[5])
            embed.add_field(name=f"**Christmas cracker** {rares['christmas_cracker']}", value=row[6])
            embed.add_field(name=f"**Red h'ween mask** {rares['red_hween']}", value=row[7])
            embed.add_field(name=f"**Blue h'ween mask** {rares['blue_hween']}", value=row[8])
            embed.add_field(name=f"**Green h'ween mask** {rares['green_hween']}", value=row[9])
            embed.add_field(name=f"**Santa hat** {rares['santa_hat']}", value=row[10])
            embed.add_field(name=f"**Pumpkin** {rares['pumpkin']}", value=row[11])
            embed.add_field(name=f"**Easter egg** {rares['easter_egg']}", value=row[12])

            await message.send(embed=embed)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("RARES ERROR", error)
    finally:
        if conn is not None:
            conn.close()
