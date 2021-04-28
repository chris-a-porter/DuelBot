import random
from random import randint
from cogs.item_files.drop_tables import common_table, uncommon_table, rare_table, super_rare_table, holiday_table


# Generate one loot item
# @input table class: PlayerKillingLootTable
def pick_loot_item(table):
    loot = random.choice(table.get())
    return loot


# Generate a loot item based on RNG (a few items)
def generate_random_loot_item():

    selected_item = None

    rng = randint(0, 999)
    if rng == 0:
        selected_item = pick_loot_item(holiday_table)
    if rng <= 5:
        selected_item = pick_loot_item(super_rare_table)
    elif rng <= 50:
        selected_item = pick_loot_item(rare_table)
    elif rng <= 250:
        selected_item = pick_loot_item(uncommon_table)
    elif rng <= 999:
        selected_item = pick_loot_item(common_table)

    return selected_item


# Generate a whole loot pile
def generate_loot_pile(min_rolls, max_rolls):

    # Dictate the amount of loot rolls the player will receive
    num_rolls = randint(min_rolls, max_rolls)

    # Track all of the loot gained
    loot = {}

    # For each roll, append the loot pile
    for _ in range(num_rolls):

        loot_item = generate_random_loot_item()
        loot_item_quantity = randint(loot_item['min'], loot_item['max'])

        if loot_item["id"] in loot:
            loot[loot_item["id"]] = loot[loot_item["id"]] + loot_item_quantity
        else:
            loot[loot_item["id"]] = loot_item_quantity

    return loot
