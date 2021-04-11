# Roll for a chance to receive a rare/holiday item
# If the rares table is hit, the user will receive a message
import psycopg2
import os
from cogs.item_files.emojis_list import rares
from random import randint

DATABASE_URL = os.environ['DATABASE_URL']


async def roll_for_rares(self, message, winner):

    item = None
    item_text = None
    item_emoji = None

    table_roll = randint(0, 74)

    # Winner hits the rares table
    # Effective rates are as follows:
        # Christmas cracker - 0.01% or 1/10,000
        # Partyhat table - 0.18% or 18/10,000
            # Red partyhat - 0.03% or 3/10,000
            # Blue partyhat - 0.03% or 3/10,000
            # Yellow partyhat - 0.03% or 3/10,000
            # Green partyhat - 0.03% or 3/10,000
            # Purple partyhat - 0.03% or 3/10,000
            # White partyhat - 0.03% or 3/10,000
        # Halloween mask table - 0.21% or 21/10,000
            # Red halloween mask - 0.07% or 7/10,000
            # Blue halloween mask - 0.07% or 7/10,000
            # Green halloween mask - 0.07% or 7/10,000
        # Santa hat - 0.10% or 10/10,000
        # Pumpkin - 0.25% or 25/10,000
        # Easter egg - 0.25% or 25/10,000

    if table_roll == 0:
        rares_roll = randint(0, 99)
        if rares_roll == 0:  # hit table for cracker
            item = "_962"
            item_text = "Christmas cracker"
            item_emoji = rares['christmas_cracker']
        elif rares_roll <= 17:  # hit table for a partyhat
            phat_roll = randint(0, 5)
            if phat_roll == 0:
                item = "_1038"
                item_text = "a Red partyhat"
                item_emoji = rares['red_partyhat']
            elif phat_roll == 1:
                item = "_1042"
                item_text = "a Blue partyhat"
                item_emoji = rares['blue_partyhat']
            elif phat_roll == 2:
                item = "_1040"
                item_text = "a Yellow partyhat"
                item_emoji = rares['yellow_partyhat']
            elif phat_roll == 3:
                item = "_1044"
                item_text = "a Green partyhat"
                item_emoji = rares['green_partyhat']
            elif phat_roll == 4:
                item = "_1046"
                item_text = "a Purple partyhat"
                item_emoji = rares['purple_partyhat']
            elif phat_roll == 5:
                item = "_1048"
                item_text = "a White partyhat"
                item_emoji = rares['white_partyhat']
        elif rares_roll <= 38:  # hit table for a mask
            mask_roll = randint(0, 2)
            if mask_roll == 0:
                item = "_1057"
                item_text = "a Red h'ween mask"
                item_emoji = rares['red_hween']
            elif mask_roll == 1:
                item = "_1055"
                item_text = "a Blue h'ween mask"
                item_emoji = rares['blue_hween']
            elif mask_roll == 2:
                item = "_1053"
                item_text = "a Green h'ween mask"
                item_emoji = rares['green_hween']
        elif rares_roll <= 49:  # hit table for a santa hat
            item = "_1050"
            item_text = "a Santa hat"
            item_emoji = rares['santa_hat']
        elif rares_roll <= 74:  # hit table for a pumpkin
            item = "_1959"
            item_text = "a Pumpkin"
            item_emoji = rares['pumpkin']
        elif rares_roll <= 99:  # hit table for an easter egg
            item = "_1961"
            item_text = "an Easter egg"
            item_emoji = rares['easter_egg']

    sql = None

    if table_roll == 0:
        print(f"{message.author.id} hit the rares table")
        sql = f"""
        INSERT INTO duel_rares (
        user_id,
        red_partyhat,
        blue_partyhat,
        yellow_partyhat,
        green_partyhat,
        purple_partyhat,
        white_partyhat,
        christmas_cracker,
        red_hween_mask,
        blue_hween_mask,
        green_hween_mask,
        santa_hat,
        pumpkin,
        easter_egg)
        VALUES
        ({winner.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        ON CONFLICT (user_id) DO UPDATE
        SET {item} = duel_rares.{item} + 1
        """
    else:
        print(f"{message.author.id} did not hit the rares table ({table_roll}/75)")
        return

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 2", error)
        return
    finally:
        if conn is not None:
            conn.close()

    # Send the message with info about hitting the rares table to the winner
    await message.send(f"**{message.author.id} received {item_text} {item_emoji} for winning!**")

    notif_channel = self.bot.get_channel(689313376286802026)
    await notif_channel.send(f"{message.author.id} has received {item_text} {item_emoji} for winning a duel!")