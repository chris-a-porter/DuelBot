from ..economy.loot.generate_loot_v2 import generate_loot_pile
from ..economy.loot.generate_loot_image import generate_loot_image


async def randomloot(ctx):
    loot_pile = generate_loot_pile(3, 5)
    await generate_loot_image(ctx, loot_pile)
