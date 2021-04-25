import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def remove_item_from_user(user, table, column_name, quantity):
    sql = f"""
    UPDATE {table}
    SET {column_name} = {column_name} - {quantity} 
    WHERE user_id = {user}
    """

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR REMOVING ITEM", error)
        return False
    finally:
        if conn is not None:
            conn.close()
        return True
