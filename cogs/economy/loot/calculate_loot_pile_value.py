from cogs.economy.item_data.fetch_price import fetch_price


async def calculate_loot_pile_value(loot_pile):

    total_value = 0

    for key in loot_pile.keys():
        item_price = await fetch_price(key)
        quantity = loot_pile[key]
        total_value = total_value + (item_price * quantity)

    return total_value
