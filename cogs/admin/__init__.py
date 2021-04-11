from discord.ext import commands
from cogs.admin.commands_givegp import give_gp


# Hub of admin-related commands. Owner only.
class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def givegp(self, ctx, *args):
        await give_gp(ctx, *args)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
