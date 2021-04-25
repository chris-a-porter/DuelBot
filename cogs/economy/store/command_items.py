import psycopg2
import os
import discord
from cogs.item_files.emojis_list import rares, chambers_of_xeric_items, saradomin_items, zamorak_items, armadyl_items, bandos_items, slayer_items, dragon_items, zulrah_items

DATABASE_URL = os.environ['DATABASE_URL']


async def command_items(ctx):
    sql = f"""
                    SELECT 
                    _13652 dragon_claws,
                    _11802 armadyl_godsword,
                    _11804 bandos_godsword,
                    _11806 saradomin_godsword,
                    _11808 zamorak_godsword,
                    _11838 saradomin_sword,
                    _4153 granite_maul,
                    _13576 dragon_warhammer,
                    _12924 toxic_blowpipe
                    FROM pking_items
                    WHERE user_id = {ctx.author.id}
                    """

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        # Get the user's GP in their coffers and set the val
        for row in rows:
            embed = discord.Embed(title=f"{ctx.author.nick}'s items", color=discord.Color.blurple())
            embed.add_field(name=f"**Dragon claws** {chambers_of_xeric_items['dragon_claws']}", value=row[0])
            embed.add_field(name=f"**Armadyl godsword** {armadyl_items['armadyl_godsword']}", value=row[1])
            embed.add_field(name=f"**Bandos godsword** {bandos_items['bandos_godsword']}", value=row[2])
            embed.add_field(name=f"**Saradomin godsword** {saradomin_items['saradomin_godsword']}", value=row[3])
            embed.add_field(name=f"**Zamorak godsword** {zamorak_items['zamorak_godsword']}", value=row[4])
            embed.add_field(name=f"**Saradomin sword** {saradomin_items['saradomin_sword']}", value=row[5])
            embed.add_field(name=f"**Granite maul** {slayer_items['granite_maul']}", value=row[6])
            embed.add_field(name=f"**Dragon warhammer** {dragon_items['dragon_warhammer']}", value=row[7])
            embed.add_field(name=f"**Toxic blowpipe** {zulrah_items['toxic_blowpipe']}", value=row[7])

            await ctx.send(embed=embed)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return
    finally:
        if conn is not None:
            conn.close()