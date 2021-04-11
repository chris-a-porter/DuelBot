import psycopg2
import os
import asyncio

DATABASE_URL = os.environ['DATABASE_URL']


async def fc(self, ctx):
    async def hasFirecape(ctx):
        sql = f"""
        SELECT
        fire_cape
        FROM user_skills
        WHERE user_id = {ctx.author.id}
        """

        # Defaults to true to stop the user from getting one
        hasFirecape = True

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            hasFirecape = cur.fetchall()
            for item in hasFirecape:
                hasFirecape = item[0]
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error beginning task", error)
        finally:
            if conn is not None:
                conn.close()

            return hasFirecape

    fc = await hasFirecape(ctx)

    if fc == True:
        await ctx.send(f"You already have a Fire cape {ItemEmojis.Misc.fireCape}")
        return

    hitpoints = await Skilling(self.bot).getLevel(ctx.author.id, 'hitpoints')
    prayer = await Skilling(self.bot).getLevel(ctx.author.id, 'prayer')
    herblore = await Skilling(self.bot).getLevel(ctx.author.id, 'herblore')
    ranged = await Skilling(self.bot).getLevel(ctx.author.id, 'ranged')

    cavesTime = 120

    await ctx.send(
        f"You step into the fight caves to take on the TzTok-Jad {ItemEmojis.Bosses.fightCaves} You should be done in about 120 minutes.")

    # Wait 2 hours
    await asyncio.sleep(60 * cavesTime)

    if hitpoints >= 70 and prayer >= 43 and herblore >= 72 and ranged >= 70:

        sql = f"""
        UPDATE user_skills
        SET fire_cape = TRUE
        WHERE user_id = {ctx.author.id}
        """

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error beginning task", error)
        finally:
            if conn is not None:
                conn.close()

        # Only give them one firecape, lol. Don't want to spam them if they used .fc a bunch of times
        hasFCmidTrip = await hasFirecape(ctx)

        if hasFCmidTrip == False:
            await ctx.send(
                f"Congratulations {ctx.author.mention}, you have received a Fire cape {ItemEmojis.Misc.fireCape} giving you a permanent **10%** boost to DPS.")
            return

    else:
        await ctx.send(
            f"{ctx.author.mention} Oh no! You died to the TzTok-Jad {ItemEmojis.Bosses.fightCaves}. You NEED get 70 Ranged {ItemEmojis.Skills.ranged}, 70 Hitpoints {ItemEmojis.Skills.hitpoints}, 72 Herblore {ItemEmojis.Skills.herblore}, and 43 Prayer {ItemEmojis.Skills.prayer} if you want to complete the Fight Caves.")
        return