import os
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']

class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')

    @commands.command(name='commands')
    async def cmds(self, message):
        return

    @commands.command()
    async def kd(self, message):
        return

    @commands.command()
    async def hs(self, ctx, *args):
        return


def setup(bot):
    bot.add_cog(UserCommands(bot))
