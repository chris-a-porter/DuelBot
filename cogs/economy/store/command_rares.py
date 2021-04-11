import discord
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def rares(self, message):
    await self.createTablesForUser(message.author)

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
            embed.add_field(name=f"**Red partyhat** {ItemEmojis.Rares.redPartyhat}", value=row[0])
            embed.add_field(name=f"**Yellow partyhat** {ItemEmojis.Rares.yellowPartyhat}", value=row[1])
            embed.add_field(name=f"**Blue partyhat** {ItemEmojis.Rares.bluePartyhat}", value=row[2])
            embed.add_field(name=f"**Green partyhat** {ItemEmojis.Rares.greenPartyhat}", value=row[3])
            embed.add_field(name=f"**Purple partyhat** {ItemEmojis.Rares.purplePartyhat}", value=row[4])
            embed.add_field(name=f"**White partyhat** {ItemEmojis.Rares.whitePartyhat}", value=row[5])
            embed.add_field(name=f"**Christmas cracker** {ItemEmojis.Rares.christmasCracker}", value=row[6])
            embed.add_field(name=f"**Red h'ween mask** {ItemEmojis.Rares.redHween}", value=row[7])
            embed.add_field(name=f"**Blue h'ween mask** {ItemEmojis.Rares.blueHween}", value=row[8])
            embed.add_field(name=f"**Green h'ween mask** {ItemEmojis.Rares.greenHween}", value=row[9])
            embed.add_field(name=f"**Santa hat** {ItemEmojis.Rares.santaHat}", value=row[10])
            embed.add_field(name=f"**Pumpkin** {ItemEmojis.Rares.pumpkin}", value=row[11])
            embed.add_field(name=f"**Easter egg** {ItemEmojis.Rares.easterEgg}", value=row[12])

            await message.send(embed=embed)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("RARES ERROR", error)
    finally:
        if conn is not None:
            conn.close()
