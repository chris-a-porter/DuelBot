import requests
import math
from .generate_pk_loot import generate_pk_loot
# Returns dict of loot


async def roll_random_loot(ctx, min_rolls, max_rolls, modifier):
    loot_dict = await generate_pk_loot(ctx, min_rolls, max_rolls, modifier)

    for itemKey in loot_dict.keys():
        url = f'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={itemKey}'

        json_response = None

        if itemKey != 995:
            response = requests.get(url)
            json_response = response.json()
        elif itemKey == 995:
            json_response = {'item':
                                {'name': 'Coins',
                                 'current':
                                     {'price': 1}
                                 }
                            }

        # Get current price of item
        # Can beformatted as x,xxx,xxx or x.xxxM/K/B
        item_price = json_response['item']['current']['price']

        # Remove commas

        value = 0

        # If the item is a string (not an int, basically)
        if type(item_price) == str:

            if ',' in item_price:
                item_price = item_price.replace(',', '')
                value = int(item_price)
            else:
                price_multiplier = float(item_price[0: -1])
                price_suffix = item_price[-1]

                if price_suffix == 'k':
                    value = math.floor(price_multiplier * 1000)
                elif price_suffix == 'm':
                    value = math.floor(price_multiplier * 1000000)
                elif price_suffix == 'b':
                    value = math.floor(price_multiplier * 1000000000)

        if type(item_price) == int:
            value = int(item_price)

        # 0 is the name of the item, 1 is the GP (int) value of the item, 2 is the item price shortened, 3 is the number of the item, 4 is the emoji
        self.lootArray[itemKey] = [json_response['item']['name'], value, item_price, loot_dict[itemKey][0],
                                   loot_dict[itemKey][1]]

    # Add the coin value of each item to the the total coins in the drop
    for item in self.lootArray.values():
        self.lootArray[995][1] = self.lootArray[995][1] + (item[1] * item[3])

    return self.lootArray