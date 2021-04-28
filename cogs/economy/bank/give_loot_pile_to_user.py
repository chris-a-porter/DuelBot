import psycopg2
from psycopg2 import extras
import os

DATABASE_URL = os.environ['DATABASE_URL']


# Add item to user's bank
async def give_loot_pile_to_user(user_id, loot_pile):

    insert_query = """INSERT INTO user_items
        (user_id, item_id, quantity)
        VALUES """

    for key in loot_pile.keys():
        insert_query = insert_query + f"({user_id}, {key}, {loot_pile[key]}),"

    # Remove last comma
    insert_query = insert_query[:-1]

    insert_query = insert_query + " ON CONFLICT (user_id, item_id) DO UPDATE SET quantity = user_items.quantity + EXCLUDED.quantity"

    print(insert_query)

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(insert_query)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR REMOVING ITEM", error)
        return False
    finally:
        if conn is not None:
            conn.close()
        return True