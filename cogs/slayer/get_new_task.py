import psycopg2
import os
import random
from random import randint
from cogs.skilling.get_level import get_level
from .get_current_slayer_master import get_current_slayer_master
from .slayer_masters import slayerMasters

DATABASE_URL = os.environ['DATABASE_URL']


async def get_new_task(user_id):
    # Get current master and slayer level
    current_master = await get_current_slayer_master(user_id)
    current_level = await get_level(user_id, 'slayer')

    task_id = None
    count = None

    # Roll to find a task that the user has the slayer level for
    ticker = 0
    while task_id is None and ticker < 1000:
        ticker = ticker + 1

        rolled_task = random.choice(list(slayerMasters[current_master]["tasks"]))

        if current_level >= slayerMasters[current_master]["tasks"][rolled_task]["req"]:
            task_id = slayerMasters[current_master]["tasks"][rolled_task]["id"]
            task_info = slayerMasters[current_master]["tasks"][rolled_task]
            count = randint(slayerMasters[current_master]["tasks"][rolled_task]["min"], slayerMasters[current_master]["tasks"][rolled_task]["max"])
            break

    sql = f"""
            UPDATE user_skills
            SET slayer_task = {task_id}, slayer_monster_count = {count}
            WHERE user_id = {user_id}
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

    return [task_id, count]
