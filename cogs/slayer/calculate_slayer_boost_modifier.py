import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def calculateModifier(userId):
    sql = f"""
    SELECT
    face_mask,
    nose_peg,
    spiny_helm,
    earmuffs,
    ice_cooler,
    bag_of_salt,
    witchwood_icon,
    insulated_boots,
    fungicide,
    slayer_gloves,
    leaf_bladed_sword,
    leaf_bladed_battleaxe,
    rock_hammer,
    mirror_shield,
    fire_cape,
    abyssal_whip,
    black_mask,
    slayer_helmet
    FROM user_skills
    WHERE user_id = {userId}
    """

    boost_data = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        for row in data:
            boost_data = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching slayer items", error)
    finally:
        if conn is not None:
            conn.close()

    multiplier = 1
    # Low items (spiny helm, ear muffs, etc)
    for n in range(0, 10):
        if boost_data[n] is True:
            multiplier = multiplier + 0.01

    # Leaf bladed sword, battleaxe, rock hammer, and mirror shield
    for n in range(10, 14):
        if boost_data[n] is True:
            multiplier = multiplier + 0.025

    # Fire cape and abyssal whip
    for n in range(14, 16):
        if boost_data[n] is True:
            multiplier = multiplier + 0.05

    # Black mask and slayer helmet
    for n in range(16, 18):
        if boost_data[n] is True:
            multiplier = multiplier + 0.10

    return [boost_data, multiplier]
