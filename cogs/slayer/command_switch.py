import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def switch(ctx, style):

    styles = ["attack", "strength", "defence", "ranged", "magic"]

    if style in styles:
        sql = f"""
        UPDATE user_skills
        SET attack_style = '{style}'
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

            await ctx.send(f"You are now gaining {style.lower().capitalize()} xp.")
            return
    else:
        await ctx.send("You can only train Attack, Strength, Defence, Ranged and magic. ")
        return