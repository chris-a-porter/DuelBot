from helpers.math_helpers import numify, short_numify
from ..store.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player
from ..bank.remove_item_from_user import remove_item_from_user
from ..bank.give_item_to_user import give_item_to_user


async def pay(ctx, *args):
    quantity = numify(args[1])

    short_quant = short_numify(quantity, 1)

    if type(quantity) != int:
        await ctx.send('Please enter a valid number.')
        return

    users_quantity = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

    if users_quantity < quantity:
        await ctx.send('You do not have enough gp to do that.')
        return

    person = args[0].replace('@', '').replace('>', '').replace('<', '').replace('!', '')

    await remove_item_from_user(ctx.author.id, 'duel_users', 'gp', quantity)
    await give_item_to_user(person, 'duel_users', 'gp', quantity)
    await ctx.send(f"You pay {short_quant} to <@!{person}>")
    return
