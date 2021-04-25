import os
from cogs.skilling.command_buybones import buy_bones
from cogs.skilling.command_buyherb import buy_herb
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']


class SkillingCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buybones(self, ctx, amount):
        await buy_bones(ctx, amount)

    @buybones.error
    async def buy_bones_error(self, ctx, error):
        await ctx.send("Proper syntax is *=buybones [GP amount]*. Prayer experience can be bought for 200 GP each.")

    @commands.command()
    async def buyherb(self, ctx, amount):
        await buy_herb(ctx, amount)

    @buyherb.error
    async def buy_herb_error(self, ctx, error):
        await ctx.send("Proper syntax is */buyherb [GP amount]*. Herblore experience can be bought for 350 GP each.")


def setup(bot):
    bot.add_cog(SkillingCommands(bot))
