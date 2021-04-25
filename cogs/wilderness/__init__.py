import os
from discord.ext import commands
from .command_pk import command_pk


class Wilderness(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pk(self, ctx, *args):
        await command_pk(ctx, *args)


def setup(bot):
    bot.add_cog(Wilderness(bot))
