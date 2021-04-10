import psycopg2
import os
from random import randint
import math
from cogs.skilling.get_level import get_level


DATABASE_URL = os.environ['DATABASE_URL']


async def kill_monsters(self, ctx, monster_id, num_left):
    taskMonster = None
    for monster in self.all_db_monsters:
        if monster.id == monster_id:
            taskMonster = monster
            break

    # Returns an [item, rate] list that can be rolled to receive an item.
    def roll_for_item(task_monster_id, numRolls):

        roll = None
        if task_monster_id == 423 or task_monster_id == 498:  # Dust devils and smoke devils
            roll = ['face_mask', 1 / 256, '1%']
        elif task_monster_id == 2:  # Aberrant spectres
            roll = ['nose_peg', 1 / 256, '1%']
        elif task_monster_id == 476:  # Wall beasts
            roll = ['spiny_helm', 1 / 256, '1%']
        elif task_monster_id == 414:  # Banshees
            roll = ['earmuffs', 1 / 256, '1%']
        elif task_monster_id == 458:  # Lizards
            roll = ['ice_cooler', 1 / 256, '1%']
        elif task_monster_id == 421:  # Rockslugs
            roll = ['bag_of_salt', 1 / 256, '1%']
        elif task_monster_id == 1047:  # Cave horrors
            # Roll up to 6. If greater than 1, roll for witchwood icon. If less than 1, roll for black mask
            rand = randint(0, 5)
            if rand > 1:
                roll = ['witchwood_icon', 4 / 512, '1%']  # Multiply 2/512 by 2 since it's 2/3 up above
            else:
                roll = ['black_mask', 3 / 512, '10%']  # Multiply by 1/512 by 3 since it's 1/3 up above
        elif task_monster_id == 2478:  # Spiders
            roll = ['slayer_gloves', 1 / 256, '1%']
        elif task_monster_id == 469:  # Killerwatts
            roll = ['insulated_boots', 1 / 256, '1%']
        elif task_monster_id == 537:  # Zygomites
            roll = ['fungicide', 1 / 256, '1%']
        elif task_monster_id == 426 or task_monster_id == 410:  # Turoths and kurasks
            if task_monster_id == 426:
                roll = ['leaf_bladed_sword', 1 / 442, '2.5%']
            elif task_monster_id == 410:
                rand = randint(0, 5)
                if rand > 1:
                    roll = ['leaf_bladed_sword', 2 / 442, '2.5%']
                else:
                    roll = ['leaf_bladed_battleaxe', 3 / 1026, '2.5%']
        elif task_monster_id == 412:  # Gargoyles
            roll = ['rock_hammer', 1 / 256, '2.5%']
        elif task_monster_id == 419 or task_monster_id == 9293:  # Cockatrices, Basilisks
            roll = ['mirror_shield', 1 / 256, '2.5%']
        elif task_monster_id == 415:  # Abyssal demons
            roll = ['abyssal_whip', 1 / 512, '5%']

        success = False
        if roll is not None:
            for n in range(0, numRolls):
                loot_roll = randint(0, math.floor(1 / roll[1]))
                if loot_roll == 0:
                    success = True
                    break

            return [roll[0], success, roll[2]]
        else:
            return None

    async def addTripTime(ctx, partTime):

        sql = f"""
          UPDATE user_skills
          SET finishtime = {time.time() + partTime}, currently_slaying = TRUE
          WHERE user_id = {ctx.author.id}
          """
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 90", error)
        finally:
            if conn is not None:
                conn.close()

    async def getAttackStyle(userId):
        sql = f"""
          SELECT
          attack_style
          FROM user_skills
          WHERE user_id = {userId}
          """

        attack_style = 1
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                attack_style = row[0]
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 90", error)
        finally:
            if conn is not None:
                conn.close()

        return attack_style

    # Calculate the DPS for the task based on user levels and monster defence
    async def calculateDPS(user_id, monsterId):
        attack = await get_level(user_id, 'attack')
        strength = await get_level(user_id, 'strength')
        defence = await get_level(user_id, 'defence')
        hitpoints = await get_level(user_id, 'hitpoints')
        ranged = await get_level(user_id, 'ranged')
        magic = await get_level(user_id, 'magic')
        prayer = await get_level(user_id, 'prayer')

        taskMonster = None
        for monster in self.all_db_monsters:
            if monster.id == monsterId:
                taskMonster = monster

        # Give an equipment bonus depending on the attack level of the player
        # Uses scimitars for reference
        equipment_bonus = 0
        if attack < 5:
            equipment_bonus = 9
        elif attack < 10:
            equipment_bonus = 14
        elif attack < 20:
            equipment_bonus = 14
        elif attack < 30:
            equipment_bonus = 20
        elif attack < 40:
            equipment_bonus = 28
        elif attack < 60:
            equipment_bonus = 44
        elif attack >= 60:
            equipment_bonus = 66

        effective_strength_level = strength + 8

        max_hit = 0.5 + effective_strength_level * (equipment_bonus + 64) / 640

        # Calculate attack bonus depending on attack level
        # Uses scimitars for reference
        attack_bonus = 0
        if attack < 5:
            equipment_bonus = 10
        elif attack < 10:
            equipment_bonus = 15
        elif attack < 20:
            equipment_bonus = 19
        elif attack < 30:
            equipment_bonus = 21
        elif attack < 40:
            equipment_bonus = 29
        elif attack < 60:
            equipment_bonus = 45
        elif attack >= 60:
            equipment_bonus = 67

        effective_attack_level = attack + 8

        max_attack_roll = effective_attack_level * (attack_bonus + 64)

        effective_monster_defence = taskMonster.defence_level + 9

        effective_monster_equipment_bonus = taskMonster.defence_slash

        max_defence_roll = effective_monster_defence * (effective_monster_equipment_bonus + 64)

        hit_chance = 0

        if max_attack_roll > max_defence_roll:
            hit_chance = 1 - (max_defence_roll + 2) / (2 * (max_attack_roll + 1))
        else:
            hit_chance = max_attack_roll / (2 * max_defence_roll + 1)

        currentStyle = await getAttackStyle(user_id)

        if currentStyle == 'attack' or currentStyle == 'strength' or currentStyle == 'defence':
            # Give an equipment bonus depending on the attack level of the player
            # Uses scimitars for reference
            equipment_bonus = 0
            if attack < 5:
                equipment_bonus = 9
            elif attack < 10:
                equipment_bonus = 14
            elif attack < 20:
                equipment_bonus = 14
            elif attack < 30:
                equipment_bonus = 20
            elif attack < 40:
                equipment_bonus = 28
            elif attack < 60:
                equipment_bonus = 44
            elif attack >= 60:
                equipment_bonus = 66

            effective_strength_level = strength + 8

            max_hit = 0.5 + effective_strength_level * (equipment_bonus + 64) / 640

            # Calculate attack bonus depending on attack level
            # Uses scimitars for reference
            attack_bonus = 0
            if attack < 5:
                equipment_bonus = 10
            elif attack < 10:
                equipment_bonus = 15
            elif attack < 20:
                equipment_bonus = 19
            elif attack < 30:
                equipment_bonus = 21
            elif attack < 40:
                equipment_bonus = 29
            elif attack < 60:
                equipment_bonus = 45
            elif attack >= 60:
                equipment_bonus = 67

            effective_attack_level = attack + 8

            max_attack_roll = effective_attack_level * (attack_bonus + 64)

            effective_monster_defence = taskMonster.defence_level + 9

            effective_monster_equipment_bonus = taskMonster.defence_slash

            max_defence_roll = effective_monster_defence * (effective_monster_equipment_bonus + 64)

            hit_chance = 0

            if max_attack_roll > max_defence_roll:
                hit_chance = 1 - (max_defence_roll + 2) / (2 * (max_attack_roll + 1))
            else:
                hit_chance = max_attack_roll / (2 * max_defence_roll + 1)

            dps = hit_chance * (max_hit / 2) / 2.4

            return dps

        elif currentStyle == 'ranged':

            rangedStrength = 4
            equipment = 0
            interval = 1.2

            if ranged < 5:  # Iron knives
                rangedStrength = 4
                equipment = 30
            elif ranged < 10:  # Steel knives
                rangedStrength = 7
                equipment = 35
            elif ranged < 20:  # Black knives
                rangedStrength = 8
                equipment = 40
            elif ranged < 30:  # Mithril knives
                rangedStrength = 10
                equipment = 45
            elif ranged < 40:  # Adamant knives
                rangedStrength = 14
                equipment = 50
            elif ranged < 50:  # Rune knives
                rangedStrength = 24
                equipment = 70
            elif ranged < 60:  # Magic shortbow, blue d'hide
                rangedStrength = 49
                equipment = 124
                interval = 2.4
            elif ranged < 70:  # Magic shortbow, red d'hide
                rangedStrength = 49
                equipment = 129
                interval = 2.4
            elif ranged < 75:  # Magic shortbow, black d'hide
                rangedStrength = 49
                equipment = 134
                interval = 2.4
            elif ranged < 85:  # Blowpipe with adamant darts
                rangedStrength = 50
                equipment = 145
                interval = 1.2
            elif ranged < 91:  # Blowpipe with rune darts
                rangedStrength = 54
                equipment = 149
                interval = 1.2
            elif ranged < 97:  # Blowpipe with dragon darts
                rangedStrength = 60
                equipment = 153
                interval = 1.2

            max_hit = 1.3 + (ranged / 10) + (rangedStrength / 80) + ((ranged * rangedStrength) / 640)

            average_hit = max_hit / 2
            max_attack_roll = ranged * (equipment + 64)
            max_defence_roll = (taskMonster.defence_level + 9) * (taskMonster.defence_ranged + 64)

            hit_chance = 0

            if max_attack_roll > max_defence_roll:
                hit_chance = 1 - (defence + 2) / (2 * (ranged + 1))
            else:
                hit_chance = ranged / (2 * defence + 1)

            dps = hit_chance * average_hit / interval

            if dps < 0.25:
                dps = dps + 0.125

            return dps

    # Calculate the user's damage % modifier
    async def calculateModifier(userId):
        sql = f"""
          SELECT
          face_mask,
          nose_peg,
          spiny_helm,
          earmuffs,
          ice_cooler,
          bag_of_salt,
          witchwood_icon,
          insulated_boots,
          fungicide,
          slayer_gloves,
          leaf_bladed_sword,
          leaf_bladed_battleaxe,
          rock_hammer,
          mirror_shield,
          fire_cape,
          abyssal_whip,
          black_mask,
          slayer_helmet
          FROM user_skills
          WHERE user_id = {userId}
          """

        boostData = None

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                boostData = row
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error fetching slayer items", error)
        finally:
            if conn is not None:
                conn.close()

        multiplier = 1
        # Low items (spiny helm, ear muffs, etc)
        for n in range(0, 10):
            if boostData[n] is True:
                multiplier = multiplier * 1.01

        # Leaf bladed sword, battleaxe, rock hammer, and mirror shield
        for n in range(10, 14):
            if boostData[n] is True:
                multiplier = multiplier * 1.025

        # Fire cape and abyssal whip
        for n in range(14, 16):
            if boostData[n] is True:
                multiplier = multiplier * 1.05

        # Black mask and slayer helmet
        for n in range(16, 18):
            if boostData[n] is True:
                multiplier = multiplier * 1.05

        async def calculatePrayerModifier(userId):
            prayer_level = await get_level(userId, 'prayer')

            modifier = 1 + (prayer_level / 198)

            if prayer_level == 99:
                modifier = modifier + 0.1

            return modifier

        async def calculateHerbloreModifier(userId):
            herblore_level = await get_level(userId, 'herblore')

            modifier = 1

            if herblore_level < 3:  # None
                modifier = 1
            elif herblore_level < 12:  # Attack
                modifier = 1.01
            elif herblore_level < 30:  # Strength
                modifier = 1.02
            elif herblore_level < 38:  # Defence
                modifier = 1.05
            elif herblore_level < 45:  # Prayer
                modifier = 1.1
            elif herblore_level < 55:  # Super attack
                modifier = 1.2
            elif herblore_level < 63:  # Super strength
                modifier = 1.3
            elif herblore_level < 66:  # Super restore
                modifier = 1.4
            elif herblore_level < 70:  # Super def
                modifier = 1.5
            elif herblore_level < 81:  # Divine combat
                modifier = 1.6
            elif herblore_level < 90:  # Brew
                modifier = 1.7
            elif herblore_level < 97:  # Super combat
                modifier = 1.8
            elif herblore_level < 99:  # Divine super combat
                modifier = 1.9
            elif herblore_level == 99:  # User has 99
                modifier = 2.0

            return modifier

        prayerMultiplier = await calculatePrayerModifier(ctx.author.id)
        herbloreMultiplier = await calculateHerbloreModifier(ctx.author.id)

        return multiplier * prayerMultiplier * herbloreMultiplier

    async def removeFromTask(userId, numberKilled):

        sql = f"""
          UPDATE user_skills
          SET slayer_monster_count = slayer_monster_count - {numberKilled}
          WHERE user_id = {userId}
          """

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 90", error)
        finally:
            if conn is not None:
                conn.close()

        return

    async def giveSlayerPoints(userId, points):
        sql = f"""
          UPDATE user_skills
          SET slayer_points = slayer_points + {points}, slayer_task_total = slayer_task_total + 1
          WHERE user_id = {userId}
          """
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 90", error)
        finally:
            if conn is not None:
                conn.close()

    # Grab the attack style
    attackStyle = await getAttackStyle(ctx.author.id)

    # Calculate beginning level for the style being used, hitpoints, and slayer
    startCombat = await get_level(ctx.author.id, attackStyle)
    startHitpoints = await get_level(ctx.author.id, 'hitpoints')
    startSlayer = await get_level(ctx.author.id, 'slayer')

    dps = await calculateDPS(ctx.author.id, monster_id)

    # Equiment modifier
    modifier = await calculateModifier(ctx.author.id)

    # Total damage dealt for the session
    totalDamage = dps * 1800 * modifier * 1.33

    # Maximum possible kills
    maxKills = math.floor(totalDamage / taskMonster.hitpoints)

    # Default to max kills...
    numberKilled = maxKills

    if numberKilled < 3:
        numberKilled = 3
        maxKills = 3

    taskMessage = f"You have **{num_left - numberKilled} {taskMonster.name}** left on your task."

    # But if the max amount of kills is greater than the amount left, just make it the amount left
    if maxKills > num_left:
        numberKilled = num_left

        # Get the current slayer master
        master = await self.getCurrentSlayerMaster(ctx.author.id)

        # Read the number of points they'll get
        points = self.slayerMasters[master]["points"]

        # Give slayer points
        await giveSlayerPoints(ctx.author.id, points)

        # If the user is getting points for their task, add it into the message.
        pointMessage = ""
        if points != 0:
            pointMessage = f"and gained **{points}** slayer points"

        taskMessage = f"You have finished your task {pointMessage}. Type *=slay task* to get a new one."
    print("Num", numberKilled / maxKills, 1800 * (numberKilled / maxKills))
    await addTripTime(ctx, math.floor(1800 * (numberKilled / maxKills)))

    # HERE BEGINS THE DATABASE WRITING STUFF

    await ctx.send(
        f"You begin slaying {taskMonster.name}s. You should return in about {math.ceil(30 * (numberKilled / maxKills))} minutes.")

    await asyncio.sleep(math.floor(1800 * (numberKilled / maxKills)))

    # Remove the monsters from the task monster count
    await removeFromTask(ctx.author.id, numberKilled)

    timeModifier = math.floor(num_left / maxKills * 1800)

    # Calculate experience for the player
    combatXP = numberKilled * taskMonster.hitpoints * 4
    commaCombatXP = "{:,d}".format(int(combatXP))
    hitpointsXP = numberKilled * taskMonster.hitpoints * 1.33
    commaHitpointsXP = "{:,d}".format(int(hitpointsXP))
    slayerXP = numberKilled * taskMonster.slayer_xp
    commaSlayerXP = "{:,d}".format(int(slayerXP))

    # End combat levels
    endCombat = await Skilling(self.bot).addExperienceToStat(ctx.author.id, attackStyle, combatXP)
    endHitpoints = await Skilling(self.bot).addExperienceToStat(ctx.author.id, 'hitpoints', hitpointsXP)
    endSlayer = await Skilling(self.bot).addExperienceToStat(ctx.author.id, 'slayer', slayerXP)

    # Level up message placeholders
    combatLevelUp = ""
    hitpointsLevelUp = ""
    slayerLevelUp = ""
    attackStyleCap = attackStyle.capitalize()

    # If the user levels up
    if endCombat > startCombat:
        combatLevelUp = f"You are now level {endCombat} {attackStyleCap}."
    if endHitpoints > startHitpoints:
        hitpointsLevelUp = f"You are now level {endHitpoints} Hitpoints."
    if endSlayer > startSlayer:
        slayerLevelUp = f"You are now level {endSlayer} Slayer."

    # The emoji corresponding to the attack style being used
    styleEmoji = None
    if attackStyle == 'attack':
        styleEmoji = ItemEmojis.Skills.attack
    elif attackStyle == 'strength':
        styleEmoji = ItemEmojis.Skills.strength
    elif attackStyle == 'defence':
        styleEmoji = ItemEmojis.Skills.defence
    elif attackStyle == 'ranged':
        styleEmoji = ItemEmojis.Skills.ranged

    itemMessage = ""

    # Roll to see if the user receives a unique slayer drop
    itemRoll = roll_for_item(taskMonster.id, numberKilled)
    if itemRoll != None:
        if itemRoll[1] == True:
            async def checkForItem(item):
                sql = f"""
                  SELECT
                  {item}
                  FROM user_skills
                  WHERE user_id = {ctx.author.id}
                  """
                itemData = False
                try:
                    conn = psycopg2.connect(DATABASE_URL)
                    cur = conn.cursor()
                    cur.execute(sql)
                    data = cur.fetchall()
                    for row in data:
                        itemData = row[0]
                    cur.close()
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Error fetching slayer items", error)
                finally:
                    if conn is not None:
                        conn.close()
                    return itemData

            async def giveItem(item):
                sql = f"""
                  UPDATE user_skills
                  SET {item} = TRUE
                  WHERE user_id = {ctx.author.id}
                  """
                itemData = False
                try:
                    conn = psycopg2.connect(DATABASE_URL)
                    cur = conn.cursor()
                    cur.execute(sql)
                    cur.close()
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Error fetching slayer items", error)
                finally:
                    if conn is not None:
                        conn.close()

            # Check to see if the user has the item
            hasItem = await checkForItem(itemRoll[0])
            if hasItem == False:
                itemName = itemRoll[0].capitalize().replace('_', ' ')
                sqlColumn = itemRoll[0]

                # Give the user the item
                await giveItem(sqlColumn)

                # Update the item message
                itemMessage = f"You have received **{itemName}** as a drop, granting a permanent **{itemRoll[2]}** boost to damage."

    message = f"{ItemEmojis.Skills.slayer} {ctx.author.mention} you have killed **{numberKilled} {taskMonster.name}**.{taskMessage}\nYou have gained:\n{commaCombatXP} {attackStyle.capitalize()} XP {styleEmoji} {combatLevelUp}\n{commaHitpointsXP} Hitpoints XP {ItemEmojis.Skills.hitpoints} {hitpointsLevelUp}\n{commaSlayerXP} Slayer XP {ItemEmojis.Skills.slayer} {slayerLevelUp}\n\n{itemMessage}"

    # Send a message with task info
    await ctx.send(message)

    async def endTrip(ctx):
        sql = f"""
          UPDATE user_skills
          SET currently_slaying = FALSE
          WHERE user_id = {ctx.author.id}
          """
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 76", error)
        finally:
            if conn is not None:
                conn.close()

    await endTrip(ctx)