import os
from random import randint
import math
from .make_hitpoints_image import make_hitpoints_image
import discord
from ..admin.commands_randomloot import roll_pking_table_loot
from ..economy.bank.give_item_to_user import give_item_to_user
from .update_db_with_duel_results import update_db_with_duel_results
from .turn_checker import turnChecker

# freezeAttack() causes the attacking user to use an attack that has potential to use the enemy
# Inputs:
# message - discord context - context of the discord bot
# weapon - string - the weapon name
# special - int - the amount of special attack the weapon uses
# rolls - int - number of hits the weapon has
# max - int - max hit of the weapon
# freezeChance - int - % chance to freeze the enemy
async def freezeAttack(ctx, weapon, special, rolls, max, freezeChance):
    # Internal vars used for reference
    sending_user = None  # User ending the attack
    receiving_user = None  # User taking damage

    # Retrieve the channel's duel from the global duel dict
    channelDuel = globals.duels.get(ctx.channel.id, None)

    if ctx.channel.id != channelDuel.channel:
        return

    # If the duel doesn't exist, just return
    if channelDuel == None:
        return

    # Sets the attacker and defender (sending_user and receiving_user, respectively)
    # If the attacker is player one
    if ctx.author.id == channelDuel.user_1.user.id:
        sending_user = channelDuel.user_1
        receiving_user = channelDuel.user_2

    # If the attacker is player two
    if ctx.author.id == channelDuel.user_2.user.id:
        sending_user = channelDuel.user_2
        receiving_user = channelDuel.user_1

    # If the user was not part of the duel
    if sending_user is None:
        return

    # If the sender is part of the duel, but it is not their turn
    # Sends a message to the discord channel stating that it is not the player's turn
    if sending_user.user.id != channelDuel.turn.user.id:
        await ctx.send("It's not your turn.")
        return

        # if the user does not have enough special attack
    if special == 0:
        pass
    elif sending_user.special < special:
        await ctx.send(f"Using the {weapon} requires {special}% special attack energy.")
        return

    # Records last attack to prevent using spamming
    # Notable exceptions include the DDS and Abyssal whip
    # TODO: Might be a good idea to just convert this into a bool parameter
    if weapon == "DDS" or weapon == "Abyssal whip":  # Exceptions
        sending_user.lastAttack = weapon
    elif sending_user.lastAttack == weapon:  # Weapon being used is the same as last time
        # Send a message to the channel that the weapon cannot be used twice in a row
        await ctx.send("You cannot use that type of attack twice in a row.")
        return
    else:
        sending_user.lastAttack = weapon

    # Array to hold the hits rolled
    hitArray = []

    # Roll a RNG hit (rolls) times and append [hitArray]
    for n in range(0, rolls):
        hit = randint(0, max)
        hitArray.append(hit)

    # Calculate poison (25% chance of 6 damage)
    # This is outside of the below code because it's used to append the final message
    poisonRoll = randint(0, 3)

    # If the receiver is already poisoned...
    if receiving_user.poisoned == True:
        # If the user is already poisoned and the poison roll succeeded, apply damage
        if poisonRoll == 0:
            receiving_user.hitpoints -= 6

    # Calculate damage dealt and subtract it from receiving_user hitpoints
    leftoverHitpoints = receiving_user.hitpoints - sum(hitArray)
    receiving_user.hitpoints = leftoverHitpoints

    # Calculate special remaining
    sending_user.special -= special

    # Roll to freeze, rounds down
    rand = randint(0, math.floor((100 / freezeChance)) - 1)

    # Creates the appropriate image to display hitpoints
    if leftoverHitpoints > 0:

        if receiving_user.poisoned == True and rand == 0:  # If the receiving_user is poisoned, and the freeze roll hit
            make_hitpoints_image(leftoverHitpoints, True, True)
        elif receiving_user.poisoned == True and rand != 0:  # If the receiving_user is poisoned and the freeze roll did not hit
            make_hitpoints_image(leftoverHitpoints, False, True)
        elif receiving_user.poisoned == False and rand == 0:  # If the receiving_user is not poisoned and the freeze roll hit
            make_hitpoints_image(leftoverHitpoints, True, False)
        elif receiving_user.poisoned == False and rand != 0:  # If the receiving_user is not poisoned and the freeze roll did not hit
            make_hitpoints_image(leftoverHitpoints, False, False)
    else:
        # If the receiving_user has 0 hitpoints left
        make_hitpoints_image(0, False, False)

    # Holds the message to send to the channel containing information about the hit, spec percentage, freeze, or death
    sending = ""

    # If the weapon only hit once (no freeze attacks currently hit more than once)
    if len(hitArray) == 1:
        sending += f'{ctx.author.id} uses **{weapon}** and hits a **{hitArray[0]}** on {receiving_user.user.id}.'

    # winning message
    if leftoverHitpoints <= 0:
        await ctx.send(
            content=f'{sending} \n**{ctx.author.id}** has won the duel with **{sending_user.hitpoints}** HP left!',
            file=discord.File('./hpbar.png'))
        await update_db_with_duel_results(sending_user.user, receiving_user.user)
        del globals.duels[ctx.channel.id]

        if channelDuel.stakeItem == None:
            await roll_pking_table_loot(ctx)
        else:
            itemToWin = channelDuel.stakeItem
            numberToWin = channelDuel.stakeQuantity * 2
            table = channelDuel.table
            if channelDuel.stakeItem == 'gp':
                await ctx.send(f"**{ctx.author.id}** has won {channelDuel.shortQuantity} GP.")
            else:
                await ctx.send(f"**{ctx.author.id}** has won {numberToWin} {channelDuel.itemLongName}.")
            await give_item_to_user(ctx.author.id, table, itemToWin, numberToWin)
        return

    # Calculates special energy remaining and adds to message
    if special != 0:
        sending += f' {ctx.author.id} has {sending_user.special}% special attack energy left.'

    # If the user got hit by poison and they're poisoned (both will be true if the user was poisoned this turn) append the message to send
    if poisonRoll == 0 and receiving_user.poisoned == True:
        sending += f' {receiving_user.user.id} is hit for **6** poison damage.'

    # If the user is frozen, send the message and return early to avoid switching who the turnChecker is looking for
    if rand == 0:
        sending += f' {receiving_user.user.id} is **frozen** and loses their turn.'
        channelDuel.turnCount += 1
        await ctx.send(sending)
        await ctx.send(file=discord.File('./hpbar.png'))
        return

    # Send the attack message and image
    await ctx.send(content=sending, file=discord.File('./hpbar.png'))

    os.remove('./hpbar.png')
    channelDuel.turnCount += 1
    await turnChecker(ctx, channelDuel)