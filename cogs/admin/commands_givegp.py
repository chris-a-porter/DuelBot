from helpers.math_helpers import numify, short_numify
from cogs.economy.store.give_item_to_user import give_item_to_user


async def give_gp(ctx, *args):

    print("ARGUMENTS HERE", ctx, *args)

    quantity = numify(args[1])

    short_quant = short_numify(quantity, 1)

    if type(quantity) != int:
        await ctx.send('Please enter a valid number.')
        return

    person = args[0].replace('@', '').replace('>', '').replace('<', '').replace('!', '')

    await give_item_to_user(person, 'duel_users', 'gp', quantity)
    await ctx.send(f"You gave {short_quant} to <@!{person}>")
    return
