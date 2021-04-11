import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def remove_gp_from_user(self, message, user_id, amount):

    if amount <= await self.checkUserGP(user_id):
        sql = f"""
        UPDATE duel_users 
        SET gp = gp - {amount} 
        WHERE user_id = {user_id}
        """
        conn = None

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("REMOVING GP ERROR", error)
            return
        finally:
            if conn is not None:
                conn.close()
            return True
    else:
        await message.send("You don't have that much GP.")
        return False
