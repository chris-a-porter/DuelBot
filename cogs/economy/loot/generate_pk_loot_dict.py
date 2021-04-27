from random import randint
import random

# Formerly rollLoot


async def generate_pk_loot_dict(ctx, min_rolls, max_rolls, modifier):
    async def pickTable():
        # Pick a random number and assign it to the table
        rng = randint(0, 599)

        table = None

        # Roll for table
        if rng <= 5:
            table = self.superRareItems
        elif rng <= 35:
            table = self.rareItems
        elif rng <= 135:
            table = self.uncommonItems
        elif rng <= 599:
            table = self.commonItems

        # Roll for random value in table -- loot is a dictionary key
        loot = random.choice(list(table.keys()))

        # Roll for random loot quantity from min/max in value for key [loot]
        lootQuantity = randint(table[loot][1], table[loot][2])

        if self.lootArray.get(loot, None) != None:
            self.lootArray[loot][0] = self.lootArray[loot][0] + lootQuantity
        elif self.lootArray.get(loot, None) == None:
            self.lootArray[loot] = [lootQuantity, table[loot][3]]  # Stores the quantity and emoji for the item

            # User his the super rare table, send notification

        if rng <= 5:
            ultraItemPrice = await Economy(self.bot).getItemValue(int(loot))
            itemPriceString = RSMathHelpers(self.bot).shortNumify(ultraItemPrice, 1)
            notifChannel = self.bot.get_channel(689313376286802026)
            await notifChannel.send(
                f"{ItemEmojis.Coins.coins} **{ctx.author.nick}** hit the ultra rare drop table and received a **{table[loot][0]}** {table[loot][3]} worth {itemPriceString} GP.")

    # Roll between 3 and 6 drops
    # Gives an additional roll to people that are a member of the main discord guild
    bonusRolls = 0
    duelArenaGuild = self.bot.get_guild(663113372580970509)
    if duelArenaGuild.get_member(ctx.author.id) != None:
        bonusRolls = 1

    rollNum = randint(min_rolls + modifier, max_rolls + modifier)

    for _ in range(0, rollNum):
        await pickTable()

    if bonusRolls == 1:
        await pickTable()

    return self.lootArray