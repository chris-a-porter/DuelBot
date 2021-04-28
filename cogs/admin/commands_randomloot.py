from ..economy.loot.generate_loot_v2 import generate_loot_pile
from ..economy.loot.generate_loot_image import generate_loot_image
from ..economy.loot.calculate_loot_pile_value import calculate_loot_pile_value
from ..economy.bank.give_loot_pile_to_user import give_loot_pile_to_user


async def roll_pking_table_loot(ctx):

    msg = await ctx.send("Checking the loot pile...")

    loot_pile = generate_loot_pile(3, 6)
    loot_pile_value = await calculate_loot_pile_value(loot_pile)

    await give_loot_pile_to_user(ctx.author.id, loot_pile)
    await generate_loot_image(ctx, loot_pile, loot_pile_value, message=msg)
