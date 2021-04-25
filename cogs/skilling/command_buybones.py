import discord
from cogs.item_files.emojis_list import prayers, skills
from cogs.economy.store.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player
from helpers.math_helpers import numify, short_numify
from cogs.economy.store.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player
from cogs.economy.bank.remove_item_from_user import remove_item_from_user
from .get_level import get_level
from .add_experience_to_stat import add_experience_to_stat
import math

# Command to purchase prayer xp


async def buy_bones(ctx, amount):
    try:
        if amount == 'info':
            # Display info about prayer
            embed = discord.Embed(title="Prayer bonuses", description="Damage multiplier based on level",
                                  color=discord.Color.from_rgb(250, 250, 250))
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/f/f2/Prayer_icon.png?ca0dc')

            description_1 = f"""{prayers['thick_skin']} Thick skin - 1 - +0%
            {prayers['burst_of_strength']} Burst of Strength - 4 - +2%
            {prayers['clarity_of_thought']} Clarity of Thought - 7 - +3.5%
            {prayers['rock_skin']} Rock Skin - 10 - +5%
            {prayers['superhuman_strength']} Superhm. Strength - 13 - +6.5%
            {prayers['improved_reflexes']} Improved Reflexes - 14 - +7%
            """
            description_2 = f"""{prayers['steel_skin']} Steel Skin - 28 - +14%
            {prayers['ultimate_strength']} Ultimate Strength - 31 - +15.5%
            {prayers['incredible_reflexes']} Incredible Reflexes - 34 - +17%
            {prayers['chivalry']} Chivalry - 60 - +30%
            {prayers['piety']} Piety - 70 - +35%
            {skills['prayer']} Mastery - 99 - 60%
            """

            description_3 = f"""Prayer experience costs **200 GP** per 1 experience
            To buy Prayer experience, use .buybones (GP amount)
    
            Your effective multiplier grows by ~0.5% per level, with a 10% bonus at 99.
            Even if your level is between upgrades, you will get a bonus. *(e.g. 80 prayer for +40%)*
            """

            embed.add_field(name='\u200b', value=description_1, inline=True)
            embed.add_field(name='\u200b', value=description_2, inline=True)
            embed.add_field(name='\u200b', value=description_3, inline=False)

            await ctx.send(embed=embed)
            return

        else:
            amount = numify(amount)
            if amount < 200:
                await ctx.send('You must purchase at least 1 xp. Each experience point costs 200 gp.')
                return

            user_gp = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

            if amount > user_gp:
                print("Here!")
                await ctx.send("You don't have that much GP.")
                return

            short_amount = short_numify(amount, 1)
            prayer_xp = math.floor(amount / 200)
            short_prayer_xp = short_numify(prayer_xp, 1)

            if type(amount) != int:

                await ctx.send("Please enter a valid amount.")

            else:
                user_gp = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

                if user_gp >= amount:

                    await remove_item_from_user(ctx.author.id, 'duel_users', 'gp', amount)

                    start_level = await get_level(ctx.author.id, 'prayer')
                    await add_experience_to_stat(ctx.author.id, 'prayer', prayer_xp)
                    end_level = await get_level(ctx.author.id, 'prayer')

                    level_up_message = ""
                    if end_level > start_level:
                        level_up_message = f"Your prayer level is now {end_level}."

                    await ctx.send(
                        f"{skills['prayer']} You have purchased {short_prayer_xp} prayer experience for {short_amount} GP. {level_up_message}")
    except Exception as e:
        print("Something went wrong", e)

