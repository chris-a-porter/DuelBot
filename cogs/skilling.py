import discord
import os
import math
import psycopg2
from cogs.osrsEmojis import ItemEmojis
from helpers.math_helpers import RSMathHelpers
from cogs.economy import Economy
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']

class Skilling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buybones(self, ctx, amount):

        if amount == 'info':
            # Display info about prayer
            embed = discord.Embed(title="Prayer bonuses", description="Damage multiplier based on level", color=discord.Color.from_rgb(250, 250, 250))
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/f/f2/Prayer_icon.png?ca0dc')

            description_1 = f"""{ItemEmojis.Prayers.thickSkin} Thick skin - 1 - +0%
            {ItemEmojis.Prayers.burstOfStrength} Burst of Strength - 4 - +2%
            {ItemEmojis.Prayers.clarityOfThought} Clarity of Thought - 7 - +3.5%
            {ItemEmojis.Prayers.rockSkin} Rock Skin - 10 - +5%
            {ItemEmojis.Prayers.superhumanStrength} Superhm. Strength - 13 - +6.5%
            {ItemEmojis.Prayers.improvedReflexes} Improved Reflexes - 14 - +7%
            """
            description_2 = f"""{ItemEmojis.Prayers.steelSkin} Steel Skin - 28 - +14%
            {ItemEmojis.Prayers.ultimateStrength} Ultimate Strength - 31 - +15.5%
            {ItemEmojis.Prayers.incredibleReflexes} Incredible Reflexes - 34 - +17%
            {ItemEmojis.Prayers.chivalry} Chivalry - 60 - +30%
            {ItemEmojis.Prayers.piety} Piety - 70 - +35%
            {ItemEmojis.Skills.prayer} Mastery - 99 - 60%
            """

            description_3 = f"""Prayer experience costs **200 GP** per 1 experience
            To buy Prayer experience, use =buybones (GP amount)

            Your effective multiplier grows by ~0.5% per level, with a 10% bonus at 99.
            Even if your level is between upgrades, you will get a bonus. *(e.g. 80 prayer for +40%)*
            """

            embed.add_field(name='\u200b', value=description_1, inline=True)
            embed.add_field(name='\u200b', value=description_2, inline=True)
            embed.add_field(name='\u200b', value=description_3, inline=False)

            await ctx.send(embed=embed)
            return

        else:
            amount = RSMathHelpers(self.bot).numify(amount)
            if amount < 200:
                await ctx.send('You must purchase at least 1 xp. Each experience point costs 200 gp.')
                return

            userGP = await Economy(self.bot).getNumberOfItem(ctx.author.id, 'duel_users', 'gp')

            if amount > userGP:
                print("Here!")
                await ctx.send("You don't have that much GP.")
                return

            print("Didn't make it here")
            shortAmount = RSMathHelpers(self.bot).shortNumify(amount, 1)
            prayerXP = math.floor(amount/200)
            shortPrayerXP = RSMathHelpers(self.bot).shortNumify(prayerXP, 1)

            if type(amount) != int:

                await ctx.send("Please enter a valid amount.")
                
            else:
                userGP = await Economy(self.bot).getNumberOfItem(ctx.author.id, 'duel_users', 'gp')

                if userGP >= amount:

                    await Economy(self.bot).removeItemFromUser(ctx.author.id, 'duel_users', 'gp', amount)

                    startLevel = await self.getLevel(ctx.author.id, 'prayer')
                    await self.addExperienceToStat(ctx.author.id, 'prayer', prayerXP)
                    endLevel = await self.getLevel(ctx.author.id, 'prayer')

                    levelUpMessage = ""
                    if endLevel > startLevel:
                        levelUpMessage = f"Your prayer level is now {endLevel}."
                    
                    await ctx.send(f"{ItemEmojis.Skills.prayer} You have purchased {shortPrayerXP} prayer experience for {shortAmount} GP. {levelUpMessage}")

    @buybones.error
    async def buyBonesError(self, ctx, error):
        await ctx.send("Proper syntax is *=buybones [GP amount]*. Prayer experience can be bought for 200 GP each.")

    @commands.command()
    async def buyherb(self, ctx, amount):

        await self.createSkillTable(ctx.author.id)

        if amount == 'info':
            # Display info about prayer
            embed = discord.Embed(title="Herblore bonuses", description="Damage multiplier based on level", color=discord.Color.green())
            embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/0/03/Herblore_icon.png?ffa9e')

            description_1 = f"""{ItemEmojis.Potions.attack} Attack potions - 3 - +1%
            {ItemEmojis.Potions.strength} Strength potions - 12 - +2%
            {ItemEmojis.Potions.defence} Defence potions - 30 - +5%
            {ItemEmojis.Potions.prayer} Prayer potions - 38 - +10%
            {ItemEmojis.Potions.superAttack} Super attack potions - 45 - +20%
            {ItemEmojis.Potions.superStrength} Super strength potions - 55 - +30%
            {ItemEmojis.Potions.superRestore} Super restore potions - 63 - +40%
            """
            description_2 = f"""{ItemEmojis.Potions.superDefence} Super defence potions - 66 - +50%
            {ItemEmojis.Potions.divineSuperStrength} Divine combat potions - 70 - +60%
            {ItemEmojis.Potions.saradominBrew} Saradomin brews - 81 - +70%
            {ItemEmojis.Potions.superCombat} Super combat potion - 90 - +80%
            {ItemEmojis.Potions.divineSuperCombat} Divine super combat potions - 90 - +90%
            {ItemEmojis.Skills.herblore} Mastery - 99 - +100%
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
            amount = RSMathHelpers(self.bot).numify(amount)
            if amount < 200:
                await ctx.send('You must purchase at least 1 xp. Each experience point costs 350 gp.')
                return

            userGP = await Economy(self.bot).getNumberOfItem(ctx.author.id, 'duel_users', 'gp')

            if amount > userGP:
                print("Here!")
                await ctx.send("You don't have that much GP.")
                return
            
            print("Didn't make it here herb")
            shortAmount = RSMathHelpers(self.bot).shortNumify(amount, 1)
            herbXP = math.floor(amount/350)
            shortHerbXp = RSMathHelpers(self.bot).shortNumify(herbXP, 1)

            if type(amount) != int:

                await ctx.send("Please enter a valid amount.")

            else:

                userGP = await Economy(self.bot).getNumberOfItem(ctx.author.id, 'duel_users', 'gp')

                if userGP >= amount:

                    await Economy(self.bot).removeItemFromUser(ctx.author.id, 'duel_users', 'gp', amount)

                    startLevel = await self.getLevel(ctx.author.id, 'herblore')
                    await self.addExperienceToStat(ctx.author.id, 'herblore', herbXP)
                    endLevel = await self.getLevel(ctx.author.id, 'herblore')

                    levelUpMessage = ""
                    if endLevel > startLevel:
                        levelUpMessage = f"Your herblore level is now {endLevel}."

                    await ctx.send(f"{ItemEmojis.Skills.herblore} You have purchased {shortHerbXp} herblore experience for {shortAmount} GP. {levelUpMessage}")

    @buyherb.error
    async def buyBonesError(self, ctx, error):
        print(error)
        await ctx.send("Proper syntax is */buyherb [GP amount]*. Herblore experience can be bought for 350 GP each.")

def setup(bot):
    bot.add_cog(Skilling(bot))
