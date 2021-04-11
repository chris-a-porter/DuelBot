import discord
from helpers.math_helpers import numify, short_numify
from cogs.item_files.emojis_list import potions, skills
from cogs.economy.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player
import math


async def buyherb(self, ctx, amount):

    if amount == 'info':
        # Display info about prayer
        embed = discord.Embed(title="Herblore bonuses", description="Damage multiplier based on level", color=discord.Color.green())
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/0/03/Herblore_icon.png?ffa9e')

        description_1 = f"""{potions['attack']} Attack potions - 3 - +1%
        {potions['strength']} Strength potions - 12 - +2%
        {potions['defence']} Defence potions - 30 - +5%
        {potions['prayer']} Prayer potions - 38 - +10%
        {potions['super_attack']} Super attack potions - 45 - +20%
        {potions['super_strength']} Super strength potions - 55 - +30%
        {potions['super_restore']} Super restore potions - 63 - +40%
        """
        description_2 = f"""{potions['super_defence']} Super defence potions - 66 - +50%
        {potions['divine_super_strength']} Divine combat potions - 70 - +60%
        {potions['saradomin_brew']} Saradomin brews - 81 - +70%
        {potions['super_combat']} Super combat potion - 90 - +80%
        {potions['divine_super_combat']} Divine super combat potions - 90 - +90%
        {skills['herblore']} Mastery - 99 - +100%
        """

        description_3 = """Herblore experience costs **350 GP** per 1 experience
        To buy Herblore experience, use =buyherb (GP amount)
        """

        embed.add_field(name='\u200b', value=description_1, inline=True)
        embed.add_field(name='\u200b', value=description_2, inline=True)
        embed.add_field(name='\u200b', value=description_3, inline=False)

        await ctx.send(embed=embed)
        return

    else:
        amount = numify(amount)
        if amount < 200:
            await ctx.send('You must purchase at least 1 xp. Each experience point costs 350 gp.')
            return

        user_gp = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

        if amount > user_gp:
            print("Here!")
            await ctx.send("You don't have that much GP.")
            return

        print("Didn't make it here herb")
        short_amount = short_numify(amount, 1)
        herb_xp = math.floor(amount / 350)
        short_herb_xp = short_numify(herb_xp, 1)

        if type(amount) != int:

            await ctx.send("Please enter a valid amount.")

        else:

            user_gp = await get_number_of_item_owned_by_player(ctx.author.id, 'duel_users', 'gp')

            if user_gp >= amount:

                await Economy(self.bot).removeItemFromUser(ctx.author.id, 'duel_users', 'gp', amount)

                startLevel = await self.getLevel(ctx.author.id, 'herblore')
                await self.addExperienceToStat(ctx.author.id, 'herblore', herb_xp)
                endLevel = await self.getLevel(ctx.author.id, 'herblore')

                levelUpMessage = ""
                if endLevel > startLevel:
                    levelUpMessage = f"Your herblore level is now {endLevel}."

                await ctx.send(
                    f"{ItemEmojis.Skills.herblore} You have purchased {short_herb_xp} herblore experience for {short_amount} GP. {levelUpMessage}")