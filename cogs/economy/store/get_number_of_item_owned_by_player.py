import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

# Returns the number of an item that belong to an user


async def get_number_of_item_owned_by_player(user_id, table, column_name):

    sql = f"""
    SELECT
    {column_name} {column_name}
    FROM {table}
    WHERE user_id = {user_id}
    """
    value = 0

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        for row in rows:
            value = row[0]

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME GETTING NUMBER OF ITEM", error)
        return 0
    finally:
        if conn is not None:
            conn.close()
        return value
