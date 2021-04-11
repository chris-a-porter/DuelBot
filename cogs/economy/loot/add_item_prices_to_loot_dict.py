import math
import requests

# Adds live prices to item dict


async def add_item_prices_to_loot_dict(self, ctx, min_rolls, max_rolls, modifier):
    loot_dict = await self.rollForLoot(ctx, min_rolls, max_rolls, modifier)

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
        itemPrice = 0

        itemPrice = json_response['item']['current']['price']

        # Remove commas

        value = 0

        # If the item is a string (not an int, basically)
        if type(itemPrice) == str:

            if ',' in itemPrice:
                itemPrice = itemPrice.replace(',', '')
                value = int(itemPrice)
            else:
                priceMultiplier = float(itemPrice[0: -1])
                priceSuffix = itemPrice[-1]

                if priceSuffix == 'k':
                    value = math.floor(priceMultiplier * 1000)
                elif priceSuffix == 'm':
                    value = math.floor(priceMultiplier * 1000000)
                elif priceSuffix == 'b':
                    value = math.floor(priceMultiplier * 1000000000)

        if type(itemPrice) == int:
            value = int(itemPrice)

        # 0 is the name of the item, 1 is the GP (int) value of the item, 2 is the item price shortened, 3 is the number of the item, 4 is the emoji
        self.lootArray[itemKey] = [json_response['item']['name'], value, itemPrice, loot_dict[itemKey][0],
                                   loot_dict[itemKey][1]]

    # Add the coin value of each item to the the total coins in the drop
    for item in self.lootArray.values():
        self.lootArray[995][1] = self.lootArray[995][1] + (item[1] * item[3])

    return self.lootArray
