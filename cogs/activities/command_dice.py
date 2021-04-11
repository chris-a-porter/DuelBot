import discord
from random import randint


async def dice(self, message, *args):
    diceAmount = 0
    helper = RSMathHelpers(self.bot)
    winStatus = ""
    try:
        helper = RSMathHelpers(self.bot)
        diceAmount = helper.numify(args[0])

        if diceAmount <= 0:
            await message.send("You can't dice less than 1 GP.")
            return
        elif diceAmount > 2000000000:
            await message.send("You can only dice up to 2B at once.")
            return

        diceAmountString = helper.shortNumify(diceAmount, 1)

        hasMoney = await helper.removeGPFromUser(message, message.author.id, diceAmount)

        if hasMoney == False:
            return

        rand = randint(1, 100)
        diceDescription = ''

        if rand >= 55:
            await helper.giveGPToUser(message, message.author.id, diceAmount * 2)
            diceDescription = f'You rolled a **{rand}** and won {diceAmountString} GP'
            winStatus = "won"
        else:
            diceDescription = f'You rolled a **{rand}** and lost {diceAmountString} GP.'
            winStatus = "lost"

        embed = discord.Embed(title='**Dice Roll**', description=diceDescription, color=discord.Color.orange())
        embed.set_thumbnail(
            url='https://vignette.wikia.nocookie.net/runescape2/images/f/f2/Dice_bag_detail.png/revision/latest?cb=20111120013858')
        await message.send(embed=embed)
    except Exception as e:
        await message.send('You must dice a valid amount.')

    # If over 100M is diced, send it to the global notifications channel
    if diceAmount >= 500000000:
        notifChannel = self.bot.get_channel(689313376286802026)
        await notifChannel.send(
            f"{ItemEmojis.Coins.coins} {message.author.id} has just diced **{helper.shortNumify(diceAmount, 1)}** and **{winStatus}**.")