import psycopg2
import os
import discord
from

DATABASE_URL = os.environ['DATABASE_URL']

def command_items(self, ctx):
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
            embed.add_field(name=f"**Dragon claws** {ItemEmojis.RaidsItems.dragonClaws}", value=row[0])
            embed.add_field(name=f"**Armadyl godsword** {ItemEmojis.Armadyl.armadylGodsword}", value=row[1])
            embed.add_field(name=f"**Bandos godsword** {ItemEmojis.Bandos.bandosGodsword}", value=row[2])
            embed.add_field(name=f"**Saradomin godsword** {ItemEmojis.Saradomin.saradominGodsword}", value=row[3])
            embed.add_field(name=f"**Zamorak godsword** {ItemEmojis.Zamorak.zamorakGodsword}", value=row[4])
            embed.add_field(name=f"**Saradomin sword** {ItemEmojis.Saradomin.saradominSword}", value=row[5])
            embed.add_field(name=f"**Granite maul** {ItemEmojis.SlayerItems.graniteMaul}", value=row[6])
            embed.add_field(name=f"**Dragon warhammer** {ItemEmojis.DragonItems.dragonWarhammer}", value=row[7])
            embed.add_field(name=f"**Toxic blowpipe** {ItemEmojis.ZulrahItems.toxicBlowpipe}", value=row[7])

            await ctx.send(embed=embed)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return
    finally:
        if conn is not None:
            conn.close()