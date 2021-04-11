import math
from random import randint
import os
import discord


async def dragon_claws_attack(self, message):
    sending_user = None
    receiving_user = None

    channel_duel = globals.duels.get(message.channel.id, None)

    if message.channel.id != channel_duel.channel:
        return

    if channel_duel is None:
        return

    if message.author.id == channel_duel.user_1.user.id:
        sending_user = channel_duel.user_1
        receiving_user = channel_duel.user_2

    if message.author.id == channel_duel.user_2.user.id:
        sending_user = channel_duel.user_2
        receiving_user = channel_duel.user_1

    if sending_user is None:
        return

    # if the wrong user is trying to go
    if sending_user.user.id != channel_duel.turn.user.id:
        await message.send("It's not your turn.")
        return

    # records last attack to prevent using spamming
    if sending_user.lastAttack == "claws":
        await message.send("You cannot use that type of attack twice in a row.")
        return
    else:
        sending_user.lastAttack = "claws"

    # if the user does not have enough special attack
    if sending_user.special < 50:
        await message.send(f"Using the Dragon claws requires 50% special attack energy.")
        return

    hits_array = []

    # calculate each damage roll
    hit = randint(0, 21)

    # if first hit 10 or higher, keep it. If it's lower, scrap it.
    if hit >= 4:
        hits_array.append(hit)  # First hit does full
        # Second hit does half of the first hit
        hits_array.append(math.floor(hit / 2))
        # Third and fourth hits do a quarter of the first hit
        hits_array.append(math.floor(hit / 4))
        hits_array.append(math.floor(hit / 4))

    else:
        hits_array.append(0)  # First hit is a 0
        second_hit = randint(0, 21)
        if second_hit >= 4:
            hits_array.append(second_hit)  # Second hit rolls for max
            # Third and fourth hits are half of second
            hits_array.append(math.floor(second_hit / 2))
            hits_array.append(math.floor(second_hit / 2))
        else:
            hits_array.append(0)  # Second hit is 0
            third_hit = randint(0, 21)
            if third_hit >= 4:
                # Third and fourth hits do 75% of max
                hits_array.append(third_hit)
                hits_array.append(third_hit - 1)
            else:
                hits_array.append(0)  # Third hit is a 0
                fourth_hit = randint(0, 21)
                if fourth_hit >= 4:
                    hits_array.append(31)  # Fourth hit is a 0
                else:
                    hits_array[2] = 1
                    hits_array.append(1)

    # calculate poison
    poison_roll = randint(0, 3)

    if receiving_user.poisoned is True:
        # if the user is already poisoned and the poison roll succeeded, apply damage.
        if poison_roll == 0:
            receiving_user.hitpoints -= 6

    # calculate damage dealt
    left_over_hitpoints = receiving_user.hitpoints - sum(hits_array)
    receiving_user.hitpoints = left_over_hitpoints

    # calculate special remaining
    sending_user.special -= 50

    # create the image for the remaining hitpoints
    if left_over_hitpoints > 0:
        if receiving_user.poisoned == True:
            self.makeImage(left_over_hitpoints, False, True)
        else:
            self.makeImage(left_over_hitpoints, False, False)
    else:
        self.makeImage(0, False, False)

    sending = ""

    sending += f'{message.author.id} uses their **Dragon claws** and hits **{hits_array[0]}-{hits_array[1]}-{hits_array[2]}-{hits_array[3]}** on {receiving_user.user.id}.'

    if poison_roll == 0 and receiving_user.poisoned == True:
        sending += f' {receiving_user.user.id} is hit for **6** poison damage.'

    # winning message
    if left_over_hitpoints <= 0:
        await message.send(
            content=f'{sending} \n**{message.author.id}** has won the duel with **{sending_user.hitpoints}** HP left!',
            file=discord.File('./hpbar.png'))
        await self.updateDB(sending_user.user, receiving_user.user)
        del globals.duels[message.channel.id]

        if channel_duel.stakeItem == None:
            await PotentialItems.generateLoot(self, message)
            await self.rollForRares(message, sending_user.user)
        else:
            item_to_win = channel_duel.stakeItem
            number_to_win = channel_duel.stakeQuantity * 2
            table = channel_duel.table
            if channel_duel.stakeItem == 'gp':
                await message.send(f"**{message.author.id}** has won {channel_duel.shortQuantity} GP.")
            else:
                await message.send(f"**{message.author.id}** has won {number_to_win} {channel_duel.itemLongName}.")
            await Economy(self.bot).giveItemToUser(message.author.id, table, item_to_win, number_to_win)
        return

    # calculates special energy remaining and adds to message
    sending += f' {message.author.id} has {sending_user.special}% special attack energy left.'

    # send message and add image below
    await message.send(content=sending, file=discord.File('./hpbar.png'))

    # remove image from local file
    os.remove('./hpbar.png')
    channel_duel.turnCount += 1
    await self.turnChecker(message, channel_duel)