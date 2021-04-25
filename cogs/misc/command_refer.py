import os
import psycopg2
from cogs.economy.store.give_item_to_user import give_item_to_user

DATABASE_URL = os.environ['DATABASE_URL']


async def refer(ctx, referral_user):

    sanitized_referral = referral_user.replace('<', '').replace('>', '').replace('@', '').replace('!', '')

    try:
        person = ctx.guild.get_member(int(sanitized_referral))
    except Exception as error:
        await ctx.send('Please tag an appropriate user using the @ symbol.')
        return

    if sanitized_referral == str(ctx.author.id):
        await ctx.send('You cannot give your referral to yourself.')
        return

    async def get_referral():
        sql = f"""
        SELECT
        referral
        FROM duel_users
        WHERE user_id = {ctx.author.id}
        """

        refer_data = None

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                refer_data = row[0]
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR OVER HERE", error)
        finally:
            if conn is not None:
                conn.close()

        return refer_data

    async def give_referral(to_user_id):
        sql = f"""
        UPDATE duel_users
        SET referral = {to_user_id}
        WHERE user_id = {ctx.author.id}
        """

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 342343", error)
        finally:
            if conn is not None:
                conn.close()

            await give_item_to_user(to_user_id, 'duel_users', 'gp', 100000000)
            await give_item_to_user(ctx.author.id, 'duel_users', 'gp', 100000000)
            await ctx.send(f'You have given your one-time referral to <@!{to_user_id}> and both of you receive 100m gp')
            return

    previous_referral = await get_referral()

    if previous_referral is not None:
        await ctx.send("You have already given out your one-time referral.")

    else:
        await give_referral(sanitized_referral)