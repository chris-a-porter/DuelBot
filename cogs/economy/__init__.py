from discord.ext import commands
from .store.command_buy import command_buy
from .store.command_sell import command_sell
from .gp.command_gp import gp
from .gp.command_pay import pay as command_pay
from .store.command_rares import command_rares
from .store.command_items import command_items


class EconomyCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gp(self, msg):
        await gp(msg)

    @commands.command()
    async def buy(self, ctx, *args):
        await command_buy(ctx, *args)

    @commands.command()
    async def sell(self, ctx, *args):
        await command_sell(ctx, *args)

    @commands.command()
    async def pay(self, ctx, *args):
        await command_pay(ctx, *args)

    @commands.command()
    async def items(self, ctx):
        await command_items(ctx)

    @commands.command()
    async def rares(self, ctx):
        await command_rares(ctx)


def setup(bot):
    bot.add_cog(EconomyCommands(bot))
