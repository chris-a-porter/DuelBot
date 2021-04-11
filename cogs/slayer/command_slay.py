import discord
import math
import time


async def slay(self, ctx, *args):
    if len(args) == 0:
        # Kill monster on task
        task = await self.getCurrentSlayerTask(ctx.author.id)

        # User does not have a task currently/has finished their last task
        if task[1] <= 0:
            await ctx.send("You do not have a task. Type *=slay task* to get a new task.")
            return
        else:

            status = await checkIfActive(ctx)

            if status == None:
                await ctx.send("Something went wrong, please try again.")
                return
            elif status == True:
                finishTime = await checkTripTime(ctx)
                timeDiff = finishTime - math.floor(time.time())
                minutes = math.floor(timeDiff / 60)
                if minutes > 0:

                    await ctx.send(f"You are currently slaying. You will be done in about {minutes} minutes.")
                    return
                else:
                    # Number of monsters
                    numLeft = task[1]

                    await self.killMonsters(ctx, task[0], task[1])

            elif status == False:
                # Number of monsters
                numLeft = task[1]

                await self.killMonsters(ctx, task[0], task[1])

    elif args[0] == 'master':

        # If there was nothing else provided
        if len(args) == 1:
            currentMaster = await self.getCurrentSlayerMaster(ctx.author.id)
            await ctx.send(
                f"""Your current slayer master is **{currentMaster.capitalize()}**.\nTo switch masters, type *=slay master [name]*\nAvailable slayer masters:\n{ItemEmojis.SlayerMasters.turael} *Turael - 3+ combat\n{ItemEmojis.SlayerMasters.mazchna} Mazchna - 20+ combat\n{ItemEmojis.SlayerMasters.vannaka} Vannaka - 40+ combat\n{ItemEmojis.SlayerMasters.chaeldar} Chaeldar - 70+ combat\n{ItemEmojis.SlayerMasters.konar} Konar - 75+ combat\n{ItemEmojis.SlayerMasters.nieve} Nieve - 85+ combat\n{ItemEmojis.SlayerMasters.duradel} Duradel - 100+ combat*""")
            return

        # Translate the argument into key for slayerMasters dictionary
        choice = args[1].lower()

        # User has entered a valid slayer master
        if choice in self.slayerMasters:

            # Get the player's combat level
            combatLevel = await Skilling(self.bot).getCombatLevel(ctx.author.id)

            # If the user's combat level is not high enough
            if combatLevel < self.slayerMasters[choice]["req"]:
                requirement = self.slayerMasters[choice]["req"]
                choice = choice.capitalize()
                await ctx.send(
                    f"You need at least **{requirement} combat** to use {choice} as a slayer master. \nYou are currently **{combatLevel} combat**.")
                return
            else:
                # User has the combat requirement
                choice = choice.capitalize()
                await self.setSlayerMaster(ctx, choice)
                return

        # If the user did not enter a valid slayer master
        else:
            # User did not enter a valid slayer master
            currentTask = await self.getCurrentSlayerTask(ctx.author.id)
            if currentTask[1] == 0:
                currentMaster = await self.getCurrentSlayerMaster(ctx.author.id)

                await ctx.send(f"""Please choose a valid slayer master.
                 {ItemEmojis.SlayerMasters.turael} *Turael - 3+ combat
                 {ItemEmojis.SlayerMasters.mazchna} Mazchna - 20+ combat
                 {ItemEmojis.SlayerMasters.vannaka} Vannaka - 40+ combat
                 {ItemEmojis.SlayerMasters.chaeldar} Chaeldar - 70+ combat
                 {ItemEmojis.SlayerMasters.konar} Konar - 75+ combat
                 {ItemEmojis.SlayerMasters.nieve} Nieve - 85+ combat
                 {ItemEmojis.SlayerMasters.duradel} Duradel - 100+ combat
                 Your current slayer master is **{currentMaster}**""")
                return
            else:
                # Prevent switching masters in the middle of a task
                await ctx.send("You cannot switch slayer masters in the middle of a task.")
                return

    elif args[0] == 'task':
        task = await self.getCurrentSlayerTask(ctx.author.id)

        # If the player has nothing left in their current task, give em' a new one
        if task[1] <= 0:
            newTask = await self.getNewTask(ctx.author.id)
            name = None

            for monster in self.all_db_monsters:
                if monster.id == newTask[0]:
                    name = monster.name
                    break

            await ctx.send(
                f"You have been assigned to kill **{newTask[1]} {name}**. Type *=slay* to begin your task.")


        # If they already have a task
        else:
            name = None
            for monster in self.all_db_monsters:

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
         **=buyherb** (GP amount) - buy {ItemEmojis.Skills.herblore} Herblore XP for 350 gp/xp
         **=buyherb info** - shows bonuses from Herblore
         **=buybones** (GP amount) - buy {ItemEmojis.Skills.prayer} Prayer XP for 200 gp/xp
         **=buybones info** - shows bonuses from Prayer
         """

        embed.add_field(name='\u200b',
                        value="**Slayer - Get tasks, train stats**\n-Monsters will randomly drop items that upgrade your kills per hour\n-Training Herblore and Prayer increases kills per hour\n-Increasing your combat stats increases your kills per hour",
                        inline=False)
        embed.add_field(name="Commands", value=description, inline=False)

        await ctx.send(embed=embed)

    elif args[0] == 'points':
        points = await self.getSlayerPoints(ctx)
        await ctx.send(f"{ItemEmojis.Skills.slayer} You have {points} slayer points.")
        return

    elif args[0] == 'cancel':
        points = await self.getSlayerPoints(ctx)

        status = await checkIfActive(ctx)

        if status == None:
            await ctx.send("Something went wrong, please try again.")
            return
        elif status == True:
            finishTime = await checkTripTime(ctx)
            timeDiff = finishTime - math.floor(time.time())
            minutes = math.floor(timeDiff / 60)
            if minutes > 0:
                await ctx.send(
                    f"You cannot cancel a task while you are currently slaying. You will be done in about {minutes} minutes.")
                return

    elif args[0] == 'items':

        boostInfo = await calculateModifier(ctx.author.id)

        modifier = boostInfo[1] - 1

        modifier = modifier * 100

        boostPercent = "{0:.2f}".format(modifier)

        ownedList = []

        for item in boostInfo[0]:
            if item == True:
                ownedList.append('**')
            elif item == False:
                ownedList.append('')

        one_percent = f"""{ItemEmojis.SlayerEquipment.faceMask} {ownedList[0]}Face mask{ownedList[0]}
         {ItemEmojis.SlayerEquipment.nosePeg} {ownedList[1]}Nose peg{ownedList[1]}
         {ItemEmojis.SlayerEquipment.spinyHelmet} {ownedList[2]}Spiny helmet{ownedList[2]}
         {ItemEmojis.SlayerEquipment.earmuffs} {ownedList[3]}Earmuffs{ownedList[3]}
         {ItemEmojis.SlayerEquipment.iceCooler} {ownedList[4]}Ice cooler{ownedList[4]}
         {ItemEmojis.SlayerEquipment.bagOfSalt} {ownedList[5]}Bag of salt{ownedList[5]}
         {ItemEmojis.SlayerEquipment.witchwoodIcon} {ownedList[6]}Witchwood icon{ownedList[6]}
         {ItemEmojis.SlayerEquipment.insulatedBoots} {ownedList[7]}Insulated boots{ownedList[7]}
         {ItemEmojis.SlayerEquipment.fungicide} {ownedList[8]}Fungicide{ownedList[8]}
         {ItemEmojis.SlayerEquipment.slayerGloves} {ownedList[9]}Slayer gloves{ownedList[9]}"""

        two_point_five_percent = f"""{ItemEmojis.SlayerEquipment.leafBladedSword} {ownedList[10]}Lead-bladed sword{ownedList[10]}
         {ItemEmojis.SlayerEquipment.leafBladedBattleaxe} {ownedList[11]}Leaf-bladed battleaxe{ownedList[11]}
         {ItemEmojis.SlayerEquipment.rockHammer} {ownedList[12]}Rock hammer{ownedList[12]}
         {ItemEmojis.SlayerEquipment.mirrorShield} {ownedList[13]}Mirror shield{ownedList[13]}"""

        five_percent = f"""{ItemEmojis.Misc.fireCape} {ownedList[14]}Fire cape{ownedList[14]}
         {ItemEmojis.SlayerItems.abyssalWhip} {ownedList[15]}Abyssal whip{ownedList[15]}"""

        ten_percent = f"""{ItemEmojis.SlayerEquipment.blackMask} {ownedList[16]}Black mask{ownedList[16]}
         {ItemEmojis.SlayerEquipment.slayerHelmet} {ownedList[17]}Slayer helmet{ownedList[17]}"""

        embed = discord.Embed(title="Slayer items", description=f"Total modifier: +{boostPercent}%",
                              color=discord.Color.dark_red())
        embed.add_field(name='1% boost', value=one_percent, inline=True)
        embed.add_field(name='2.5% boost', value=two_point_five_percent, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='5% boost', value=five_percent, inline=True)
        embed.add_field(name='10% boost', value=ten_percent, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)

        await ctx.send(embed=embed)
        return
