from discord.ext import commands
from cogs.activities.command_dice import dice
import time


class ActivitiesCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def dice(self, msg, *args):
        await dice(self.bot, msg, *args)


def setup(bot):
    bot.add_cog(ActivitiesCommands(bot))
