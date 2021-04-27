import random
from random import randint
from cogs.item_files.emojis_list import rares
from cogs.item_files.drop_tables import common_table, uncommon_table, rare_table, super_rare_table


# Generate one loot item
# @input table class: PlayerKillingLootTable
def pick_loot_item(table):
    loot = random.choice(table.get())
    return loot


# Generate a loot item based on RNG (a few items)
def generate_random_loot_item():

    selected_item = None

    rng = randint(0, 599)

    if rng <= 5:
        selected_item = pick_loot_item(super_rare_table)
    elif rng <= 35:
        selected_item = pick_loot_item(rare_table)
    elif rng <= 135:
        selected_item = pick_loot_item(uncommon_table)
    elif rng <= 599:
        selected_item = pick_loot_item(common_table)

    return selected_item


# Generate a holiday drop
def generate_random_holiday_item():
    table_roll = randint(0, 74)
    item = None
    item_text = None
    item_emoji = None


    # Winner hits the rares table
    # Effective rates are as follows:
    # Christmas cracker - 0.01% or 1/10,000
    # Partyhat table - 0.18% or 18/10,000
    # Red partyhat - 0.03% or 3/10,000
    # Blue partyhat - 0.03% or 3/10,000
    # Yellow partyhat - 0.03% or 3/10,000
    # Green partyhat - 0.03% or 3/10,000
    # Purple partyhat - 0.03% or 3/10,000
    # White partyhat - 0.03% or 3/10,000
    # Halloween mask table - 0.21% or 21/10,000
    # Red halloween mask - 0.07% or 7/10,000
    # Blue halloween mask - 0.07% or 7/10,000
    # Green halloween mask - 0.07% or 7/10,000
    # Santa hat - 0.10% or 10/10,000
    # Pumpkin - 0.25% or 25/10,000
    # Easter egg - 0.25% or 25/10,000

    if table_roll == 0:
        rares_roll = randint(0, 99)
        if rares_roll == 0:  # hit table for cracker
            item = "_962"
            item_text = "Christmas cracker"
            item_emoji = rares['christmas_cracker']
        elif rares_roll <= 17:  # hit table for a partyhat
            phat_roll = randint(0, 5)
            if phat_roll == 0:
                item = "_1038"
                item_text = "a Red partyhat"
                item_emoji = rares['red_partyhat']
            elif phat_roll == 1:
                item = "_1042"
                item_text = "a Blue partyhat"
                item_emoji = rares['blue_partyhat']
            elif phat_roll == 2:
                item = "_1040"
                item_text = "a Yellow partyhat"
                item_emoji = rares['yellow_partyhat']
            elif phat_roll == 3:
                item = "_1044"
                item_text = "a Green partyhat"
                item_emoji = rares['green_partyhat']
            elif phat_roll == 4:
                item = "_1046"
                item_text = "a Purple partyhat"
                item_emoji = rares['purple_partyhat']
            elif phat_roll == 5:
                item = "_1048"
                item_text = "a White partyhat"
                item_emoji = rares['white_partyhat']
        elif rares_roll <= 38:  # hit table for a mask
            mask_roll = randint(0, 2)
            if mask_roll == 0:
                item = "_1057"
                item_text = "a Red h'ween mask"
                item_emoji = rares['red_hween']
            elif mask_roll == 1:
                item = "_1055"
                item_text = "a Blue h'ween mask"
                item_emoji = rares['blue_hween']
            elif mask_roll == 2:
                item = "_1053"
                item_text = "a Green h'ween mask"
                item_emoji = rares['green_hween']
        elif rares_roll <= 49:  # hit table for a santa hat
            item = "_1050"
            item_text = "a Santa hat"
            item_emoji = rares['santa_hat']
        elif rares_roll <= 74:  # hit table for a pumpkin
            item = "_1959"
            item_text = "a Pumpkin"
            item_emoji = rares['pumpkin']
        elif rares_roll <= 99:  # hit table for an easter egg
            item = "_1961"
            item_text = "an Easter egg"
            item_emoji = rares['easter_egg']


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

    holiday_roll = randint(0, 249)

    if holiday_roll == 0:
        loot.append(generate_random_holiday_item())

    return loot
