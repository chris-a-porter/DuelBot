from helpers.math_helpers import numify, short_numify
from cogs.economy.store.give_item_to_user import give_item_to_user
from cogs.economy.gp.give_gp_to_user import give_gp_to_user


async def give_gp(ctx, *args):

    quantity = numify(args[1])

    short_quant = short_numify(quantity, 1)

    if type(quantity) != int:
        await ctx.send('Please enter a valid number.')
        return

    # id of the user
    person = args[0].replace('@', '').replace('>', '').replace('<', '').replace('!', '')

    await give_gp_to_user(ctx, quantity)
    await ctx.send(f"You gave {short_quant} to <@!{person}>")
    return
