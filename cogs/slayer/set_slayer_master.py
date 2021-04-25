import psycopg2
import os
from .get_current_slayer_task import get_current_slayer_task

DATABASE_URL = os.environ['DATABASE_URL']


async def set_slayer_master(ctx, master):
    master_name = master.lower().capitalize()
    current_task = await get_current_slayer_task(ctx.author.id)
    if current_task[1] != 0:
        await ctx.send("You cannot switch slayer masters in the middle of a task.")
        return
    else:
        sql = F"""
        UPDATE user_skills
        SET slayer_master = '{master.lower()}'
        WHERE user_id = {ctx.author.id}
        """

        # List element containing the user's slayer experience
        master = None

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 69", error)
        finally:
            if conn is not None:
                conn.close()
            await ctx.send(f"You are now receiving tasks from {master_name}.")