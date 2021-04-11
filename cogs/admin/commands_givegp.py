async def givegp(self, ctx, *args):
    quantity = args[1]
    quantity = RSMathHelpers(self.bot).numify(args[1])

    shortQuant = RSMathHelpers(self.bot).shortNumify(quantity, 1)

    if type(quantity) != int:
        await ctx.send('Please enter a valid number.')
        return

    person = args[0].replace('@', '').replace('>', '').replace('<', '').replace('!', '')

    await Economy(self.bot).giveItemToUser(person, 'duel_users', 'gp', quantity)
    await ctx.send(f"You gave {shortQuant} to <@!{person}>")
    return
