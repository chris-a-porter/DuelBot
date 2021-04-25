import discord
from random import randint
import math
import psycopg2
import os
import random
import asyncio
import time
from cogs.item_files.emojis_list import misc_items, rares, armadyl_items, bandos_items, zamorak_items, saradomin_items, chambers_of_xeric_items, slayer_items, dragon_items, zulrah_items
from cogs.economy.loot.roll_random_loot import roll_random_loot
from cogs.economy.bank.remove_item_from_user import remove_item_from_user
from cogs.economy.bank.give_item_to_user import give_item_to_user
from helpers.math_helpers import short_numify
from .scry import scry
import globals

DATABASE_URL = os.environ['DATABASE_URL']


async def command_pk(ctx, *args, locations):

    location_list = ['wests', 'easts', 'mb', 'edge', 'lavas', 'revs', 'scry']

    # If the given location isn't in the location list
    # Send a message about how to use the =pk command
    if len(args) == 0 or args[0].lower() not in location_list:
        description = """Use .pk (region) to select a region to PK in.
        If there are other players in your region, there is a chance to pk them for their items, rares, or GP.
        You receive **extra loot** for pking at revs, lavas, and the mage bank, and for being a part of our server.
        *example: "=pk revs"*"""
        embed = discord.Embed(title='PKing commands', description=description, color=discord.Color.greyple())
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/a/a1/Skull_%28status%29_icon.png?fa6d8')
        embed.add_field(name='Regions', value='**wests** | **easts** | **mb** | **edge** | **lavas** | **revs**',
                        inline=False)
        embed.add_field(name='Utility',
                        value='**scry** - view how many players in each region \n'
                              '**kd** - view your pk stats (COMING SOON)',
                        inline=False)
        await ctx.send(embed=embed)
        return

    # If the first argument is to scry, run the scry command
    if args[0].lower() == 'scry':
        await scry()
        return

    time_status = await checkTripTime(ctx.author.id)

    if time_status[0] == 'pking' and (math.floor(time.time()) - time_status[1]) > 1200:
        await endTripSQL(ctx.author.id)

    # Catch a situation where an user has never performed an activity
    if time_status[0] == 'idle' or time_status[0] == None:
        await startTripSQL(ctx.author.id)

    # If the current time minus the time the activity started is less than 30 seconds apart, return this stuff
    elif time_status[0] != 'idle':
        time_diff = math.floor(time.time()) - time_status[1]
        minutes = 20 - math.floor(time_diff / 60)
        if minutes <= 0:
            await endTripSQL(ctx.author.id)
            await ctx.send(f"You are currently out {time_status[0]}. You should be back in less than a minute.")
            return
        else:
            await ctx.send(
                f"You are currently out {time_status[0]}. You should be back in around {minutes} minutes or less.")
            return

    locations[args[0].lower()]['players'].append(ctx.author.id)

    def convertToLongName(short):
        if short == 'wests':
            return 'Wests'
        if short == 'easts':
            return 'Easts'
        if short == 'mb':
            return 'the Mage bank'
        if short == 'edge':
            return 'Edgeville'
        if short == 'lavas':
            return 'Lava Dragon Isle'
        if short == 'revs':
            return 'the Revenant caves'
        else:
            return short

    await ctx.send(
        f'You head out on a PK trip to {convertToLongName(args[0])}. You should return in 20 minutes or less.')

    # Every 4 min, 59 secs attempt to pk another player
    for n in range(1, 4):

        # Wait 4 minutes, 55 seconds
        await asyncio.sleep(4 * 59)

        # Grab the user's status (were they pked?)
        activityInfo = await checkTripTime(ctx.author.id)

        # If they're still pking
        if activityInfo[0] == 'pking':
            # Roll to see if they killed a player
            await rollPlayerKills(ctx, args[0])
        else:
            # If the trip is over (they got pked between their rolls)
            return

    loot = None
    if args[0] == 'revs' or args[0] == 'lavas' or args[0] == 'mb':
        loot = await roll_random_loot(ctx, 3, 5, 1)
    else:
        loot = await roll_random_loot(ctx, 3, 5, 0)

    sql = f"""
    UPDATE duel_users 
    SET gp = gp + {loot[995][1]} 
    WHERE user_id = {ctx.author.id}
    """
    conn = None

    # Give the user their gold
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 3", error)
    finally:
        if conn is not None:
            conn.close()

        # Create the message that details the loot that the user received
        lootMessage = ""
        for item in loot.values():
            if item[0] != 'Coins':

                each = ''

                if item[3] > 1 and type(item[2]) != int:
                    each = ' each'

                lootMessage += f"*{item[3]}x {item[4]} {item[0]} worth {item[2]} GP{each}* \n"

        comma_money = "{:,d}".format(loot[995][1])
        lootMessage += f"Total pking trip loot value: **{comma_money} GP** {misc_items['coins']}"
        embed = discord.Embed(title=f"**Pking trip loot for {ctx.author.nick}:**", description=lootMessage,
                              thumbnail='https://oldschool.runescape.wiki/images/a/a1/Skull_%28status%29_icon.png?fa6d8')

        # End the user's trip in the database
        await endTripSQL(ctx.author.id)

        # Send a message to the server stating
        await ctx.send(f"{ctx.author.mention} you have returned from your pking trip. Type **y** to go out again.",
                       embed=embed)

        locations[args[0].lower()]["players"].remove(ctx.author.id)

        # Check the timeout to see if the user wants to run another trip
        def timeoutCheck(message):
            return message.content.lower() == 'y' and message.author.id == ctx.author.id

        # Async timeout check
        try:
            await bot.wait_for('message', check=timeoutCheck, timeout=200)
            await pk(ctx, args[0])
        except Exception as e:
            pass

def addPlayerToRegion(region, player):
    globals.locations[region]["players"].append(player)

def removePlayerFromRegion(region, player):
    globals.locations[region]["players"].remove(player)

async def checkTripTime(userId):

    sql = f"""
    SELECT
    activitystatus,
    activitytime
    FROM duel_users
    WHERE user_id = {userId}
    """

    conn = None
    activityInfo = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            activityInfo = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 90", error)
    finally:
        if conn is not None:
            conn.close()

    return row

# Updates the DB to show the latest activity begin time
async def startTripSQL(userId):

    now = math.floor(time.time())

    sql = f"""
    UPDATE duel_users
    SET 
    activitystatus = 'pking',
    activitytime = {now}
    WHERE user_id = {userId}
    """

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 25", error)
    finally:
        if conn is not None:
            conn.close()

async def endTripSQL(userId):

    print(f"Ending pking trip for {userId}")

    sql = f"""
    UPDATE duel_users
    SET 
    activitystatus = 'idle'
    WHERE user_id = {userId}
    """

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 34", error)
    finally:
        if conn is not None:
            conn.close()

async def stealOpponentsLoot(winner, loser):
    sql = f"""
        SELECT
        DU.user_id,
        DU.gp,
        DR._1038,
        DR._1040,
        DR._1042,
        DR._1044,
        DR._1046,
        DR._1048,
        DR._962,
        DR._1053,
        DR._1055,
        DR._1057,
        DR._1050,
        DR._1959,
        DR._1961,
        PI._13652,
        PI._11802,
        PI._11804,
        PI._11806,
        PI._11808,
        PI._11838,
        PI._4153,
        PI._13576,
        PI._12924

        FROM ((duel_users DU
        LEFT JOIN duel_rares DR ON DU.user_id = DR.user_id)
        LEFT JOIN pking_items PI ON DU.user_id = PI.user_id)
        WHERE DU.user_id = {loser}
        """

    itemRow = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            itemRow = row
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 3", error)
    finally:
        if conn is not None:
            conn.close()

        # Check to see if the user has... any items or gp at all
        if len(list(filter(lambda x: x != 0, itemRow[1:23]))) == 0:
            # If they have absolutely no gp, rares, or items
            return False

        coins = itemRow[1]
        raresList = itemRow[2:14]
        itemList = itemRow[15:23]

        choices = [coins, coins, coins, itemList, itemList, raresList]

        # If the
        if len(list(filter(lambda x: x != 0, raresList))) == 0:
            choices = list(filter(lambda x: x == raresList, choices))
        if len(list(filter(lambda x: x != 0, itemList))) == 0:
            choices = list(filter(lambda x: x == itemList, choices))
        if coins == 0:
            choices = list(filter(lambda x: x == coins, choices))

        print('Length of choices:', len(choices), " ||| ", choices)
        if len(choices) == 0:
            # All options were removed, user has no gp, rares, or items
            return False

        tableRoll = random.choice(choices)

        # user_id is index 0

        # Roll until you hit a number in the array that isn't 0
        def rollForItem(myList, listName):
            roll = randint(0, len(myList) - 1)
            if myList[roll] == 0:
                rollForItem(myList, listName)
            else:
                return [roll, 1, listName]

        rolledItem = None

        while rolledItem == None:
            if tableRoll == raresList:
                print('Rolling the rares table')
                # Rolled the rares table
                # Indeces include 2-14
                rolledItem = rollForItem(raresList, 'duel_rares')
                print("Rolled item in tableRoll", rolledItem)

            elif tableRoll == itemList:
                print('Rolling the items table')
                # Rolled the items table
                # Indeces include 15-23
                rolledItem = rollForItem(itemList, 'pking_items')
                print("Rolled item in tableRoll", rolledItem)

                # Steal 1 of the item

            elif tableRoll == coins:
                print('Rolling the gp table')
                # Rolled the gp Table
                # Index 1
                # Steal between 0 and 1/10th of the player's GP net worth
                rolledItem = [0, randint(0, math.floor(coins * 0.1)), 'duel_users']

        # Formatted as [index, quantity, table]
        # e.g. [5, 1, 'pking_items']
        def convertToSQL():
            index = rolledItem[0]
            quantity = rolledItem[1]
            table = rolledItem[2]

            completeInfo = {}

            # Convert the roll into SQL query-able information (the right colmumn)
            if table == 'duel_users':
                completeInfo['column'] = 'gp'
                completeInfo['emoji'] = misc_items['coins']
                completeInfo['itemName'] = 'gp'

            elif table == 'duel_rares':

                info = None
                itemName = None
                emoji = None

                if index == 0:
                    info = '_1038'
                    itemName = 'Red partyhat'
                    emoji = rares['red_partyhat']
                elif index == 1:
                    info = '_1040'
                    itemName = 'Yellow partyhat'
                    emoji = rares['yellow_partyhat']
                elif index == 2:
                    info = '_1042'
                    itemName = 'Blue partyhat'
                    emoji = rares['blue_partyhat']
                elif index == 3:
                    info = '_1044'
                    itemName = 'Green partyhat'
                    emoji = rares['green_partyhat']
                elif index == 4:
                    info = '_1046'
                    itemName = 'Purple partyhat'
                    emoji = rares['purple_partyhat']
                elif index == 5:
                    info = '_1048'
                    itemName = 'White partyhat'
                    emoji = rares['white_partyhat']
                elif index == 6:
                    info = '_962'
                    itemName = 'Christmas cracker'
                    emoji = rares['christmas_cracker']
                elif index == 7:
                    info = '_1057'
                    itemName = 'Red halloween mask'
                    emoji = rares['red_hween']
                elif index == 8:
                    info = '_1055'
                    itemName = 'Blue halloween mask'
                    emoji = rares['blue_hween']
                elif index == 9:
                    info = '_1053'
                    itemName = 'Green halloween mask'
                    emoji = rares['green_hween']
                elif index == 10:
                    info = '_1050'
                    itemName = 'Santa hat'
                    emoji = rares['santa_hat']
                elif index == 11:
                    info = '_1959'
                    itemName = 'Pumpkin'
                    emoji = rares['pumpkin']
                elif index == 12:
                    info = '_1961'
                    itemName = 'Easter egg'
                    emoji = rares['easter_egg']

                completeInfo['column'] = info
                completeInfo['emoji'] = emoji
                completeInfo['itemName'] = itemName

            elif table == 'pking_items':

                info = None
                itemName = None
                emoji = None

                if index == 0:
                    info = '_13652'
                    itemName = 'Dragon claws'
                    emoji = chambers_of_xeric_items['dragon_claws']
                elif index == 1:
                    info = '_11802'
                    itemName = 'Armadyl godsword'
                    emoji = armadyl_items['armadyl_godsword']
                elif index == 2:
                    info = '_11804'
                    itemName = 'Bandos godsword'
                    emoji = bandos_items['bandos_godsword']
                elif index == 3:
                    info = '_11806'
                    itemName = 'Saradomin godsword'
                    emoji = saradomin_items['saradomin_godsword']
                elif index == 4:
                    info = '_11808'
                    itemName = 'Zamorak godsword'
                    emoji = zamorak_items['zamorak_item']
                elif index == 5:
                    info = '_11838'
                    itemName = 'Saradomin sword'
                    emoji = saradomin_items['saradomin_sword']
                elif index == 6:
                    info = '_4153'
                    itemName = 'Granite maul'
                    emoji = slayer_items['granite_maul']
                elif index == 7:
                    info = '_13576'
                    itemName = 'Dragon warhammer'
                    emoji = dragon_items['dragon_warhammer']
                elif index == 8:
                    info = '_12924'
                    itemName = 'Toxic blowpipe'
                    emoji = zulrah_items['toxic_blowpipe']

                completeInfo['column'] = info
                completeInfo['emoji'] = emoji
                completeInfo['itemName'] = itemName

            return completeInfo

        itemDict = convertToSQL()
        itemDict['quantity'] = rolledItem[1]

        await remove_item_from_user(loser, rolledItem[2], itemDict['column'], rolledItem[1])
        await give_item_to_user(winner, rolledItem[2], itemDict['column'], rolledItem[1])

        return itemDict

async def rollPlayerKills(ctx, region):
    # Iterate through each region
    for region, data in globals.locations.items():

        for player in data["players"]:

            # Create a version of the play array that doesn't include the current player being rolled
            data_copy = data["players"].copy()
            data_copy.remove(player)
            playerListMinusCurrent = data_copy

            # Number of players in the region
            num_players_in_region = len(playerListMinusCurrent)

            # Base chance of running into another player in the region
            modifier = 128

            # Calculate chance of running into another player
            if num_players_in_region < 96:
                modifier = modifier - num_players_in_region
            else:
                modifier = 32

            # Roll the chance of finding another player
            # 0 means that another player is found
            # Minimum chance: 0.78% (for 1 other player)
            # Maximum chance: 3.125% (for 96+ other players)
            roll = randint(0, modifier)

            # If the player found another opponent in the wilderness
            if roll == 0:

                # Pick a random player to attack
                player_roll = randint(0, num_players_in_region - 1)

                # Find the attacked player
                attacked_player = playerListMinusCurrent[player_roll]

                # Pick a winner for the fight
                winner = random.choice([player, attacked_player])

                # Remove the attacked player from the regional player list
                # The attacking player was removed earlier when we ceated playerListMinusCurrent
                print("START: Attempting to remove players from list", data["players"])
                data["players"].remove(player)
                data["players"].remove(attacked_player)
                print("END: Attempting to remove players from list", data["players"])

                loser = None

                #
                if winner == player:
                    loser = attacked_player
                elif winner == attacked_player:
                    loser = player

                # Update SQL status for the winner
                await endTripSQL(winner)

                # Update SQL status for the lower
                await endTripSQL(loser)

                # Steal the item
                stolen_item = await stealOpponentsLoot(winner, loser)

                # Sort the quantity of the item (most likely 1, but if it's gp it will format)
                quant = short_numify(stolen_item['quantity'], 1)

                # Send message notifying person that their item has been stolem
                await ctx.send(
                    f"<@!{winner}> has killed <@!{loser}> for **{quant} {stolen_item['itemName']}** {stolen_item['emoji']}")

                # Get the nicknames of the winner and loser
                guildList = {}
                for guild in self.bot.guilds:
                    if guild.get_member(winner) != None:
                        guildList['winner'] = guild.get_member(winner)

                    if guild.get_member(loser) != None:
                        guildList['loser'] = guild.get_member(loser)

                # Send a notification to the notifications channel
                notifChannel = self.bot.get_channel(689313376286802026)
                await notifChannel.send(
                    f"**{guildList['winner'].nick}** has killed **{guildList['loser'].nick}** for **{stolen_item['quantity']} {stolen_item['itemName']}** {stolen_item['emoji']}")

                # Return successful player kill attempt
                return True