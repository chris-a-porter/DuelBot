import psycopg2
import os
from .add_item_data_to_database import add_item_data_to_database
DATABASE_URL = os.environ['DATABASE_URL']


async def fetch_price(item_id, is_first=True):
    sql = F"""SELECT id, price FROM item_references WHERE id={item_id}"""

    # List element containing the user's slayer experience
    row = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error finding item with ID: {item_id}", error)
    finally:
        if conn is not None:
            conn.close()

    if row is None:
        row_added = await add_item_data_to_database(item_id)

        if row_added is True and is_first is True:
            return await fetch_price(item_id, is_first=False)

        return 0

    if row is None and is_first is True:
        row_added = await add_item_data_to_database(item_id)

        if row_added is True:
            return await fetch_price(item_id, is_first=False)

        return 0

    price = row[1]

    return price
