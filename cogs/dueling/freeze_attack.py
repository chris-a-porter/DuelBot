# freezeAttack() causes the attacking user to use an attack that has potential to use the enemy
# Inputs:
# message - discord context - context of the discord bot
# weapon - string - the weapon name
# special - int - the amount of special attack the weapon uses
# rolls - int - number of hits the weapon has
# max - int - max hit of the weapon
# freezeChance - int - % chance to freeze the enemy
async def freezeAttack(self, message, weapon, special, rolls, max, freezeChance):
    # Internal vars used for reference
    sendingUser = None  # User ending the attack
    receivingUser = None  # User taking damage

    # Retrieve the channel's duel from the global duel dict
    channelDuel = globals.duels.get(message.channel.id, None)

    if message.channel.id != channelDuel.channel:
        return

    # If the duel doesn't exist, just return
    if channelDuel == None:
        return

    # Sets the attacker and defender (sendingUser and receivingUser, respectively)
    # If the attacker is player one
    if message.author.id == channelDuel.user_1.user.id:
        sendingUser = channelDuel.user_1
        receivingUser = channelDuel.user_2

    # If the attacker is player two
    if message.author.id == channelDuel.user_2.user.id:
        sendingUser = channelDuel.user_2
        receivingUser = channelDuel.user_1

    # If the user was not part of the duel
    if sendingUser == None:
        return

    # If the sender is part of the duel, but it is not their turn
    # Sends a message to the discord channel stating that it is not the player's turn
    if sendingUser.user.id != channelDuel.turn.user.id:
        await message.send("It's not your turn.")
        return

        # if the user does not have enough special attack
    if special == 0:
        pass
    elif sendingUser.special < special:
        await message.send(f"Using the {weapon} requires {special}% special attack energy.")
        return

    # Records last attack to prevent using spamming
    # Notable exceptions include the DDS and Abyssal whip
    # TODO: Might be a good idea to just convert this into a bool parameter
    if weapon == "DDS" or weapon == "Abyssal whip":  # Exceptions
        sendingUser.lastAttack = weapon
    elif sendingUser.lastAttack == weapon:  # Weapon being used is the same as last time
        # Send a message to the channel that the weapon cannot be used twice in a row
        await message.send("You cannot use that type of attack twice in a row.")
        return
    else:
        sendingUser.lastAttack = weapon

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
    if receivingUser.poisoned == True:
        # If the user is already poisoned and the poison roll succeeded, apply damage
        if poisonRoll == 0:
            receivingUser.hitpoints -= 6

    # Calculate damage dealt and subtract it from receivingUser hitpoints
    leftoverHitpoints = receivingUser.hitpoints - sum(hitArray)
    receivingUser.hitpoints = leftoverHitpoints

    # Calculate special remaining
    sendingUser.special -= special

    # Roll to freeze, rounds down
    rand = randint(0, math.floor((100 / freezeChance)) - 1)

    # Creates the appropriate image to display hitpoints
    if leftoverHitpoints > 0:

        if receivingUser.poisoned == True and rand == 0:  # If the receivingUser is poisoned, and the freeze roll hit
            self.makeImage(leftoverHitpoints, True, True)
        elif receivingUser.poisoned == True and rand != 0:  # If the receivingUser is poisoned and the freeze roll did not hit
            self.makeImage(leftoverHitpoints, False, True)
        elif receivingUser.poisoned == False and rand == 0:  # If the receivingUser is not poisoned and the freeze roll hit
            self.makeImage(leftoverHitpoints, True, False)
        elif receivingUser.poisoned == False and rand != 0:  # If the receivingUser is not poisoned and the freeze roll did not hit
            self.makeImage(leftoverHitpoints, False, False)
    else:
        # If the receivingUser has 0 hitpoints left
        self.makeImage(0, False, False)

    # Holds the message to send to the channel containing information about the hit, spec percentage, freeze, or death
    sending = ""

    # If the weapon only hit once (no freeze attacks currently hit more than once)
    if len(hitArray) == 1:
        sending += f'{message.author.id} uses **{weapon}** and hits a **{hitArray[0]}** on {receivingUser.user.id}.'

    # winning message
    if leftoverHitpoints <= 0:
        await message.send(
            content=f'{sending} \n**{message.author.id}** has won the duel with **{sendingUser.hitpoints}** HP left!',
            file=discord.File('./hpbar.png'))
        await self.updateDB(sendingUser.user, receivingUser.user)
        del globals.duels[message.channel.id]

        if channelDuel.stakeItem == None:
            await PotentialItems.generateLoot(self, message)
            await self.rollForRares(message, sendingUser.user)
        else:
            itemToWin = channelDuel.stakeItem
            numberToWin = channelDuel.stakeQuantity * 2
            table = channelDuel.table
            if channelDuel.stakeItem == 'gp':
                await message.send(f"**{message.author.id}** has won {channelDuel.shortQuantity} GP.")
            else:
                await message.send(f"**{message.author.id}** has won {numberToWin} {channelDuel.itemLongName}.")
            await Economy(self.bot).giveItemToUser(message.author.id, table, itemToWin, numberToWin)
        return

    # Calculates special energy remaining and adds to message
    if special != 0:
        sending += f' {message.author.id} has {sendingUser.special}% special attack energy left.'

    # If the user got hit by poison and they're poisoned (both will be true if the user was poisoned this turn) append the message to send
    if poisonRoll == 0 and receivingUser.poisoned == True:
        sending += f' {receivingUser.user.id} is hit for **6** poison damage.'

    # If the user is frozen, send the message and return early to avoid switching who the turnChecker is looking for
    if rand == 0:
        sending += f' {receivingUser.user.id} is **frozen** and loses their turn.'
        channelDuel.turnCount += 1
        await message.send(sending)
        await message.send(file=discord.File('./hpbar.png'))
        return

    # Send the attack message and image
    await message.send(content=sending, file=discord.File('./hpbar.png'))

    os.remove('./hpbar.png')
    channelDuel.turnCount += 1
    await self.turnChecker(message, channelDuel)