import asyncio
import discord
import os
import random
import math
import psycopg2
import time
from datetime import datetime
from cogs.item_files.emojis_list import misc_items
from helpers.math_helpers import short_numify
import threading
import schedule
from discord.ext import commands
from cogs.economy.bank.remove_item_from_user import remove_item_from_user
from cogs.economy.bank.give_item_to_user import give_item_to_user
from cogs.economy.store.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player

DATABASE_URL = os.environ['DATABASE_URL']


class Lottery(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        schedstop = threading.Event()

        def timer():
            while not schedstop.is_set():
                schedule.run_pending()
                time.sleep(3)

        schedthread = threading.Thread(target=timer)
        schedthread.start()

        # Works off of UTC --> 5PM PST is 0:00,  7PM is 02:00
        schedule.every().day.at("01:00").do(bot.loop.call_soon_threadsafe, self.runPickWinnerThread)
        # schedule.every().day.at("13:00").do(bot.loop.call_soon_threadsafe, self.runPickWinnerThread)

    async def total_tickets(self):

        print('attempting to pick winner!')
        total_tickets = 0
        ticket_array = []

        def pickWinnerFromArray():
            if len(ticket_array) > 0:
                return random.choice(ticket_array)
            else:
                return None

        sql = """
        SELECT
        user_id,
        nick,
        numTickets
        FROM lottery
        """
        conn = None

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(row)
                total_tickets += row[2]
                for n in range(1, row[2]):
                    ticket_array.append([row[0], row[1], row[2]])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return
        finally:
            if conn is not None:
                conn.close()

        def clearWinnerDB():
            sql = "DELETE FROM lottery"
            conn = None

            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql)
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return
            finally:
                if conn is not None:
                    conn.close()

        # Pick a winner
        winner_list = pickWinnerFromArray()

        # Calculate the prize money
        total_prize = short_numify((total_tickets * 4500000) + 100000000, 1)

        # Log that someone won the lottery
        print(f"Lottery winner chosen! {winner_list[0]} wins {total_prize}")

        # Give the winner their prize money
        await give_item_to_user(winner_list[0], 'duel_users', 'gp', (total_tickets * 4500000) + 100000000)

        # Send notification to the #notifications channel of the lottery winner
        notif_channel = self.bot.get_channel(689313376286802026)
        await notif_channel.send(
            f"**{winner_list[1]}** has won the lottery worth **{total_prize}**! \n The next lottery will be in 12 hours. Use *.lottery buy (quantity)* to buy tickets for 5m each.")

        # Empty the lottery DB
        clearWinnerDB()

    def runPickWinnerThread(self):
        asyncio.run_coroutine_threadsafe(self.pickWinner(), self.bot.loop)

    @commands.command()
    async def lottery(self, ctx, *args):

        quantity = None
        if len(args) > 0:
            if args[0] == 'buy':
                quantity = int(args[1])

        async def getNumTickets():

            def timeUntilNoon():
                now = datetime.now()
                today = datetime.now()
                lotto_end_pm = datetime(year=today.year, month=today.month, day=today.day, hour=1, minute=0, second=0)

                pm_delta = lotto_end_pm - now

                delta = pm_delta

                seconds = delta.seconds
                hours = math.floor(seconds / 3600)
                minutes = math.floor((seconds / 60) % 60)
                time_seconds = math.ceil(seconds - (hours * 3600) - (minutes * 60))

                return [hours, minutes, time_seconds]

            sql = """
            SELECT
            numTickets
            FROM lottery
            """
            conn = None
            total_tickets = 0

            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    total_tickets += row[0]
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            total_prize = short_numify((total_tickets * 4500000) + 100000000, 1)
            time_left = timeUntilNoon()

            sql2 = f"""
            SELECT
            numTickets
            FROM lottery
            WHERE user_id = {ctx.author.id}
            """
            conn = None
            user_tickets = 0

            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql2)
                rows = cur.fetchall()
                for row in rows:
                    user_tickets += row[0]
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

                description = f"""You have purchased **{user_tickets}** tickets 
                Total tickets in lottery: **{total_tickets}**
                Total lottery prize: **{total_prize}**
                Lottery ends in {time_left[0]} hours, {time_left[1]} minutes, and {time_left[2]} seconds."""

                embed = discord.Embed(title="DuelBot lottery", description=description, color=discord.Color.gold())
                embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/5/52/Castle_wars_ticket.png?190d3')
                await ctx.send(embed=embed)

        async def purchaseTicket(numTicks):

            # Check to see if the quantity is an integer
            try:
                quantity = int(numTicks)
            except:
                await ctx.send('You must purchase a whole number of tickets.')
                return False

            # SQL query
            sql = f"""
            INSERT INTO lottery (user_id, nick, numTickets) 
            VALUES 
            ({ctx.author.id}, '{ctx.author.id}', {numTicks}) 
            ON CONFLICT (user_id) DO UPDATE 
            SET numTickets = lottery.numTickets + {numTicks}
            """
            conn = None

            # Count the number of tickets purchased
            total_tickets = 0

            # Execute sql
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql)
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                await ctx.send('Your tickets could not be purchased.')
                return False
            finally:
                if conn is not None:
                    conn.close()
            await remove_item_from_user(ctx.author.id, 'duel_users', 'gp', numTicks * 5000000)
            cost = short_numify(numTicks * 5000000, 1)
            await ctx.send(f'You have purchased {numTicks} lottery tickets {misc_items["ticket"]} for {cost} gp')
            return True

        if len(args) == 0:
            await getNumTickets()
        # If the comand is to buy a ticket and there is a valid quantity being purchased
        elif args[0] == 'buy' and type(quantity) == int:

            # Get the user's current FP
            user_gp = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

            # Verify the user has enough gp to make the purchase
            if user_gp >= quantity * 5000000:
                # Attempt to purchase the ticket if the user has enough gp
                success = await purchaseTicket(quantity)
                if success is False:
                    return
            else:
                # Return a message saying the user doesn't have enough gp
                cost = short_numify(quantity * 5000000, 1)
                await ctx.send(f"You need {cost} gp to purchase {quantity} lottery tickets.")
                return

        # If the command is to get info about the lottery
        elif args[0] == 'info':
            await getNumTickets()

        # User wants more info about the lottery
        elif args[0] == 'help':
            message = """
            ```Lottery commands
            =lottery buy (number) - buys lottery tickets for 5m gp each
            =lottery or .lottery info - shows information about the current lottery```
            """

            await ctx.send(message)


def setup(bot):
    bot.add_cog(Lottery(bot))
