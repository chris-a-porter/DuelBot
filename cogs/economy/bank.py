import discord
from discord.ext import commands
import os
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']


class Bank:

    def __init__(self, bot, user):
        self.bot = bot
        self.user = user

    # Remove item from user's bank
    async def remove_item(self, table, column_name, quantity):
        sql = f"""
        UPDATE {table}
        SET {column_name} = {column_name} - {quantity} 
        WHERE user_id = {self.user}
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

    # Add item to user's bank
    async def give_item(self, table, column_name, quantity):

        sql = f"""
        UPDATE {table}
        SET {column_name} = {column_name} + {quantity} 
        WHERE user_id = {self.user}
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