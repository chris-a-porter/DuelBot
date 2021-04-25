from discord.ext import commands
from cogs.dueling.create_duel import create_duel


class DuelCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fight(self, ctx):
        await create_duel(ctx)

def setup(bot):
    bot.add_cog(DuelCommands(bot))
