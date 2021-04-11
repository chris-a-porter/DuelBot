import os
from discord.ext import commands
from cogs.economy.economy import buy
from cogs.economy.economy import sell

DATABASE_URL = os.environ['DATABASE_URL']

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Creates the appropriate item tables for users when using item commands

    @commands.command()
    async def buy(self, ctx, *args):
        await buy(self, ctx, *args)

    @buy.error
    async def buy_error(self, ctx, error):
        await ctx.send("Something went wrong when buying that item.")

    @commands.command()
    async def sell(self, ctx, *args):
        await sell(self, ctx, *args)

    @sell.error
    async def buy_error(self, ctx, error):
        await ctx.send("Something went wrong when selling that item.")


def setup(bot):
    bot.add_cog(Economy(bot))
