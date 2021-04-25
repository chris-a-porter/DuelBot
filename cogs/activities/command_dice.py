import discord
from random import randint
from helpers.math_helpers import numify, short_numify
from cogs.economy.gp.remove_gp_from_user import remove_gp_from_user
from cogs.economy.gp.give_gp_to_user import give_gp_to_user
from cogs.item_files.emojis_list import misc_items


async def dice(bot, message, *args):
    dice_amount = 0
    win_status = ""
    try:
        dice_amount = numify(args[0])

        if dice_amount <= 0:
            await message.send("You can't dice less than 1 GP.")
            return
        elif dice_amount > 2000000000:
            await message.send("You can only dice up to 2B at once.")
            return

        dice_amount_string = short_numify(dice_amount, 1)

        has_money = await remove_gp_from_user(message, message.author.id, dice_amount)

        if has_money is False:
            await message.send("You do not have that much GP.")
            return

        rand = randint(1, 100)
        dice_description = ''

        if rand >= 55:
            await give_gp_to_user(message, message.author.id, dice_amount * 2)
            dice_description = f'You rolled a **{rand}** and won {dice_amount_string} GP'
            win_status = "won"
        else:
            dice_description = f'You rolled a **{rand}** and lost {dice_amount_string} GP.'
            win_status = "lost"

        embed = discord.Embed(title='**Dice Roll**', description=dice_description, color=discord.Color.orange())
        embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/runescape2/images/f/f2/Dice_bag_detail.png/revision/latest?cb=20111120013858')
        await message.send(embed=embed)
    except Exception as e:
        await message.send('You must dice a valid amount.')

    # If over 100M is diced, send it to the global notifications channel
    if dice_amount >= 500000000:
        notif_channel = bot.get_channel(689313376286802026)
        await notif_channel.send(
            f"{misc_items['coins']} {message.author.id} has just diced **{short_numify(dice_amount, 1)}** and **{win_status}**.")