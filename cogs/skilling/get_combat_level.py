import psycopg2
import os
import math
from cogs.skilling.get_level import get_level

DATABASE_URL = os.environ['DATABASE_URL']


async def getCombatLevel(self, user_id):
    # Get user's stats from SQL
    attack = await get_level(user_id, 'attack')
    strength = await get_level(user_id, 'strength')
    defence = await get_level(user_id, 'defence')
    hitpoints = await get_level(user_id, 'hitpoints')
    ranged = await get_level(user_id, 'ranged')
    magic = await get_level(user_id, 'magic')
    prayer = await get_level(user_id, 'prayer')

    # Calculate the combat attributed to each stat
    base = 0.25 * (defence + hitpoints + math.floor(prayer / 2))
    melee_level = 0.325 * (attack + strength)
    ranged_level = 0.325 * (math.floor(3 * ranged / 2))
    magic_level = 0.325 * (math.floor(3 * magic / 2))

    # Calculate final combat level
    combat_level = math.floor(base + max([melee_level, ranged_level, magic_level]))

    # Return combat level
    return combat_level
