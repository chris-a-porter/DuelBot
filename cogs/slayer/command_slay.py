import discord
import math
import time
import globals
from ..item_files.emojis_list import slayer_masters, skills, slayer_equipment, misc_items, slayer_items
from .check_trip_time import checkTripTime
from .check_if_currently_slaying import check_if_currently_slaying
from .get_current_slayer_task import get_current_slayer_task
from .kill_monsters import kill_monsters
from .get_current_slayer_master import get_current_slayer_master
from .slayer_masters import slayerMasters
from .set_slayer_master import set_slayer_master
from .get_new_task import get_new_task
from .get_slayer_points import get_slayer_points
from .calculate_slayer_boost_modifier import calculateModifier
from ..skilling.get_combat_level import get_combat_level


async def command_slay(ctx, *args):
    if len(args) == 0:
        # Kill monster on task
        task = await get_current_slayer_task(ctx.author.id)

        # User does not have a task currently/has finished their last task
        if task[1] <= 0:
            await ctx.send("You do not have a task. Type *=slay task* to get a new task.")
            return
        else:

            status = await check_if_currently_slaying(ctx)

            if status is None:
                await ctx.send("Something went wrong, please try again.")
                return
            elif status is True:
                finish_time = await checkTripTime(ctx)
                time_diff = finish_time - math.floor(time.time())
                minutes = math.floor(time_diff / 60)
                if minutes > 0:

                    await ctx.send(f"You are currently slaying. You will be done in about {minutes} minutes.")
                    return
                else:
                    # Number of monsters
                    num_left = task[1]

                    await kill_monsters(ctx, task[0], task[1])

            elif status is False:
                # Number of monsters
                num_left = task[1]

                await kill_monsters(ctx, task[0], task[1])

    elif args[0] == 'master':

        # If there was nothing else provided
        if len(args) == 1:
            current_master = await get_current_slayer_master(ctx.author.id)
            await ctx.send(
                f"""Your current slayer master is **{current_master.capitalize()}**.\nTo switch masters, type *=slay master [name]*\nAvailable slayer masters:\n{slayer_masters['turael']} *Turael - 3+ combat\n{slayer_masters['mazchna']} Mazchna - 20+ combat\n{slayer_masters['vannaka']} Vannaka - 40+ combat\n{slayer_masters['chaeldar']} Chaeldar - 70+ combat\n{slayer_masters['konar']} Konar - 75+ combat\n{slayer_masters['nieve']} Nieve - 85+ combat\n{slayer_masters['duradel']} Duradel - 100+ combat*""")
            return

        # Translate the argument into key for slayerMasters dictionary
        choice = args[1].lower()

        # User has entered a valid slayer master
        if choice in slayerMasters:

            # Get the player's combat level
            combat_level = await get_combat_level(ctx.author.id)

            # If the user's combat level is not high enough
            if combat_level < slayerMasters[choice]["req"]:
                requirement = slayerMasters[choice]["req"]
                choice = choice.capitalize()
                await ctx.send(
                    f"You need at least **{requirement} combat** to use {choice} as a slayer master. \nYou are currently **{combat_level} combat**.")
                return
            else:
                # User has the combat requirement
                choice = choice.capitalize()
                await set_slayer_master(ctx, choice)
                return

        # If the user did not enter a valid slayer master
        else:
            # User did not enter a valid slayer master
            current_task = await get_current_slayer_task(ctx.author.id)
            if current_task[1] == 0:
                current_master = await get_current_slayer_master(ctx.author.id)

                await ctx.send(f"""Please choose a valid slayer master.
                 {slayer_masters['turael']} *Turael - 3+ combat
                 {slayer_masters['mazchna']} Mazchna - 20+ combat
                 {slayer_masters['vannaka']} Vannaka - 40+ combat
                 {slayer_masters['chaeldar']} Chaeldar - 70+ combat
                 {slayer_masters['konar']} Konar - 75+ combat
                 {slayer_masters['nieve']} Nieve - 85+ combat
                 {slayer_masters['duradel']} Duradel - 100+ combat
                 Your current slayer master is **{current_master}**""")
                return
            else:
                # Prevent switching masters in the middle of a task
                await ctx.send("You cannot switch slayer masters in the middle of a task.")
                return

    elif args[0] == 'task':
        task = await get_current_slayer_task(ctx.author.id)

        # If the player has nothing left in their current task, give em' a new one
        if task[1] <= 0:
            new_task = await get_new_task(ctx.author.id)
            name = None

            for monster in globals.all_db_monsters:
                if monster.id == new_task[0]:
                    name = monster.name
                    break

            await ctx.send(
                f"You have been assigned to kill **{new_task[1]} {name}**. Type *=slay* to begin your task.")


        # If they already have a task
        else:
            name = None
            for monster in globals.all_db_monsters:

                if monster.id == task[0]:
                    name = monster.name
                    break

            await ctx.send(f"You already have a task. You have **{task[1]} {name}** left.")

    elif args[0] == 'info':
        embed = discord.Embed(title=f"Slayer information", color=discord.Color.dark_red())
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/2/28/Slayer_icon.png?cd34f')

        description = f"""**=slay task** - pick up a new slayer task
         **=slay** - kill monsters in current task
         **=slay cancel** - cancels current task, (cannot cancel once task is accepted via =slay)
         **=slay points** - displays users current points
         **=slay master** - view current slayer master
         **=slay master (new master)** - switch to a new slayer master. Requires appropriate combat level.
         **=switch (attack/strength/defence/ranged/magic)** - switch to training a different skill
         **=mystats** - view current stats
         **=buyherb** (GP amount) - buy {skills['herblore']} Herblore XP for 350 gp/xp
         **=buyherb info** - shows bonuses from Herblore
         **=buybones** (GP amount) - buy {skills['prayer']} Prayer XP for 200 gp/xp
         **=buybones info** - shows bonuses from Prayer
         """

        embed.add_field(name='\u200b',
                        value="**Slayer - Get tasks, train stats**\n-Monsters will randomly drop items that upgrade your kills per hour\n-Training Herblore and Prayer increases kills per hour\n-Increasing your combat stats increases your kills per hour",
                        inline=False)
        embed.add_field(name="Commands", value=description, inline=False)

        await ctx.send(embed=embed)

    elif args[0] == 'points':
        points = await get_slayer_points(ctx)
        await ctx.send(f"{skills['slayer']} You have {points} slayer points.")
        return

    elif args[0] == 'cancel':
        points = await get_slayer_points(ctx)

        status = await check_if_currently_slaying(ctx)

        if status is None:
            await ctx.send("Something went wrong, please try again.")
            return
        elif status is True:
            finish_time = await checkTripTime(ctx)
            time_diff = finish_time - math.floor(time.time())
            minutes = math.floor(time_diff / 60)
            if minutes > 0:
                await ctx.send(
                    f"You cannot cancel a task while you are currently slaying. You will be done in about {minutes} minutes.")
                return

    elif args[0] == 'items':

        boost_info = await calculateModifier(ctx.author.id)

        modifier = boost_info[1] - 1

        modifier = modifier * 100

        boost_percent = "{0:.2f}".format(modifier)

        owned_list = []

        for item in boost_info[0]:
            if item is True:
                owned_list.append('**')
            elif item is False:
                owned_list.append('')

        one_percent = f"""{slayer_equipment['face_mask']} {owned_list[0]}Face mask{owned_list[0]}
         {slayer_equipment['nose_peg']} {owned_list[1]}Nose peg{owned_list[1]}
         {slayer_equipment['spiny_helmet']} {owned_list[2]}Spiny helmet{owned_list[2]}
         {slayer_equipment['ear_muffs']} {owned_list[3]}Earmuffs{owned_list[3]}
         {slayer_equipment['ice_cooler']} {owned_list[4]}Ice cooler{owned_list[4]}
         {slayer_equipment['bag_of_salt']} {owned_list[5]}Bag of salt{owned_list[5]}
         {slayer_equipment['witchwood_icon']} {owned_list[6]}Witchwood icon{owned_list[6]}
         {slayer_equipment['insulated_boots']} {owned_list[7]}Insulated boots{owned_list[7]}
         {slayer_equipment['fungicide']} {owned_list[8]}Fungicide{owned_list[8]}
         {slayer_equipment['slayer_gloves']} {owned_list[9]}Slayer gloves{owned_list[9]}"""

        two_point_five_percent = f"""{slayer_equipment['leaf_bladed_sword']} {owned_list[10]}Lead-bladed sword{owned_list[10]}
         {slayer_equipment['leaf_bladed_battleaxe']} {owned_list[11]}Leaf-bladed battleaxe{owned_list[11]}
         {slayer_equipment['rock_hammer']} {owned_list[12]}Rock hammer{owned_list[12]}
         {slayer_equipment['mirror_shield']} {owned_list[13]}Mirror shield{owned_list[13]}"""

        five_percent = f"""{misc_items['fire_cape']} {owned_list[14]}Fire cape{owned_list[14]}
         {slayer_items['abyssal_whip']} {owned_list[15]}Abyssal whip{owned_list[15]}"""

        ten_percent = f"""{slayer_equipment['black_mask']} {owned_list[16]}Black mask{owned_list[16]}
         {slayer_equipment['slayer_helmet']} {owned_list[17]}Slayer helmet{owned_list[17]}"""

        embed = discord.Embed(title="Slayer items", description=f"Total modifier: +{boost_percent}%",
                              color=discord.Color.dark_red())
        embed.add_field(name='1% boost', value=one_percent, inline=True)
        embed.add_field(name='2.5% boost', value=two_point_five_percent, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='5% boost', value=five_percent, inline=True)
        embed.add_field(name='10% boost', value=ten_percent, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        await ctx.send(embed=embed)
        return
