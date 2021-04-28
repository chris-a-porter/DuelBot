import globals
from random import randint
import math
from .make_hitpoints_image import make_hitpoints_image
from .turn_checker import turnChecker
from .update_db_with_duel_results import update_db_with_duel_results
from ..admin.commands_randomloot import roll_pking_table_loot
import discord
from ..economy.bank.give_item_to_user import give_item_to_user
import os


async def use_attack(message, weapon, special, rolls, max, healpercent, poison):
    sendingUser = None
    receivingUser = None

    channelDuel = globals.duels.get(message.channel.id, None)

    if message.channel.id != channelDuel.channel:
        return

    if channelDuel == None:
        return

    if message.author.id == channelDuel.user_1.user.id:
        sendingUser = channelDuel.user_1
        receivingUser = channelDuel.user_2

    if message.author.id == channelDuel.user_2.user.id:
        sendingUser = channelDuel.user_2
        receivingUser = channelDuel.user_1

    if sendingUser == None:
        return

    # if the wrong user is trying to go

    if sendingUser.user.id != channelDuel.turn.user.id:
        await message.send("It's not your turn.")
        return

    # records last attack to prevent using spamming
    if weapon == "DDS" or weapon == "Abyssal whip":
        sendingUser.lastAttack = weapon
    elif sendingUser.lastAttack == weapon:
        await message.send("You cannot use that type of attack twice in a row.")
        return
    else:
        sendingUser.lastAttack = weapon

    # if the user does not have enough special attack
    if special == 0:
        pass
    elif sendingUser.special < special:
        await message.send(f"Using the {weapon} requires {special}% special attack energy.")
        return

    hitArray = []

    # calculate each damage roll
    for n in range(0, rolls):
        hit = randint(0, max)
        hitArray.append(hit)

    # calculate poison
    poisonRoll = randint(0, 3)

    if poison == True and receivingUser.poisoned == False:
        if poisonRoll == 0:  # checks roll to see if the user is now poisoned. If yes, apply damage.
            receivingUser.poisoned = True
            receivingUser.hitpoints -= 6
    elif receivingUser.poisoned == True:
        # if the user is already poisoned and the poison roll succeeded, apply damage.
        if poisonRoll == 0:
            receivingUser.hitpoints -= 6

    # calculate damage dealt
    leftoverHitpoints = receivingUser.hitpoints - sum(hitArray)
    receivingUser.hitpoints = leftoverHitpoints

    # calculate special remaining
    sendingUser.special -= special

    # calculate any healing
    healAmount = math.floor(healpercent / 100 * hitArray[0])

    # sets lowest possible heal for SGS
    if weapon == "Saradomin godsword" and healAmount < 10:
        healAmount = 10

    # prevents healing over 99 HP
    if sendingUser.hitpoints + healAmount < 99:
        sendingUser.hitpoints += healAmount
    else:
        sendingUser.hitpoints = 99

    # create the image for the remaining hitpoints
    if leftoverHitpoints > 0:
        if receivingUser.poisoned == True:
            make_hitpoints_image(leftoverHitpoints, False, True)
        else:
            make_hitpoints_image(leftoverHitpoints, False, False)
    else:
        make_hitpoints_image(0, False, False)

    sending = ""

    # 1 attack roll
    if len(hitArray) == 1:
        sending += f'{message.author.id} uses their **{weapon}** and hits **{hitArray[0]}** on {receivingUser.user.id}.'

    # 2 attack rolls
    if len(hitArray) == 2:
        sending += f'{message.author.id} uses their **{weapon}** and hits **{hitArray[0]}-{hitArray[1]}** on {receivingUser.user.id}.'

    # 3 attack rolls
    if len(hitArray) == 3:
        sending += f'{message.author.id} uses their **{weapon}** and hits **{hitArray[0]}-{hitArray[1]}-{hitArray[2]}** on {receivingUser.user.id}.'

    if poisonRoll == 0 and receivingUser.poisoned == True:
        sending += f' {receivingUser.user.id} is hit for **6** poison damage.'

    # healing message
    if healpercent > 0:
        sending = f'{message.author.id} uses their **{weapon}** and hits **{hitArray[0]}**, healing for **{healAmount}**. {sendingUser.user.id} now has **{sendingUser.hitpoints}** HP.'

    # winning message
    if leftoverHitpoints <= 0:
        await message.send(
            content=f'{sending} \n**{message.author.id}** has won the duel with **{sendingUser.hitpoints}** HP left!',
            file=discord.File('./hpbar.png'))
        await update_db_with_duel_results(sendingUser.user, receivingUser.user)
        del globals.duels[message.channel.id]

        if channelDuel.stakeItem == None:
            await roll_pking_table_loot(message)
        else:
            itemToWin = channelDuel.stakeItem
            numberToWin = channelDuel.stakeQuantity * 2
            table = channelDuel.table
            if channelDuel.stakeItem == 'gp':
                await message.send(f"**{message.author.id}** has won {channelDuel.shortQuantity} GP.")
            else:
                await message.send(f"**{message.author.id}** has won {numberToWin} {channelDuel.itemLongName}.")
            await give_item_to_user(message.author.id, table, itemToWin, numberToWin)
        return

    # calculates special energy remaining and adds to message
    if special != 0:
        sending += f' {message.author.id} has {sendingUser.special}% special attack energy left.'

    # send message and add image below
    await message.send(content=sending, file=discord.File('./hpbar.png'))

    # Remove image from local file
    os.remove('./hpbar.png')

    # Tick up the turn counter
    channelDuel.turnCount += 1

    # Start the timer to check if another turn is taken
    await turnChecker(message, channelDuel)