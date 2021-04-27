from random import randint


# Player killing loot table
class PlayerKillingLootTable:
    def __init__(self):
        self.items = []

    def get(self):
        return self.items

    def add_item(self, item_id, min_quant, max_quant):
        self.items.append({"id": item_id, "min": min_quant, "max": max_quant})
        return self

    def roll_items(self, num_rolls):

        loot = {}

        for _ in num_rolls:

            item = randint(0, len(self.items))

            quantity = randint(item.min, item.max)

            # Increment loot quantity in dict or add to dict
            if item in loot.keys():
                loot[item] = loot[item] + quantity
            else:
                loot[item] = quantity

        return loot

