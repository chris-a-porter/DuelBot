from discord.ext import commands
from cogs.admin.commands_givegp import give_gp
from .commands_randomloot import roll_pking_table_loot
import os


PREFIX = os.environ['PREFIX']


# Hub of admin-related commands. Owner only.
class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def givegp(self, ctx, *args):
        await give_gp(ctx, *args)

    @givegp.error
    async def givegp_error(self, ctx):
        await ctx.send(f"Proper format is {PREFIX}givegp [@user] [amount]")

    @commands.command()
    @commands.is_owner()
    async def randomloot(self, ctx):
        await roll_pking_table_loot(ctx)



def setup(bot):
    bot.add_cog(AdminCommands(bot))
