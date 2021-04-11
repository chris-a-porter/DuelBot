async def pay(self, ctx, *args):
    quantity = args[1]
    quantity = RSMathHelpers(self.bot).numify(args[1])

    shortQuant = RSMathHelpers(self.bot).shortNumify(quantity, 1)

    if type(quantity) != int:
        await ctx.send('Please enter a valid number.')
        return

    usersQuantity = await Economy(self.bot).getNumberOfItem(ctx.author.id, 'duel_users', 'gp')

    if usersQuantity < quantity:
        await ctx.send('You do not have enough gp to do that.')
        return

    person = args[0].replace('@', '').replace('>', '').replace('<', '').replace('!', '')

    await Economy(self.bot).removeItemFromUser(ctx.author.id, 'duel_users', 'gp', quantity)
    await Economy(self.bot).giveItemToUser(person, 'duel_users', 'gp', quantity)
    await ctx.send(f"You give {shortQuant} to <@!{person}>")
    return