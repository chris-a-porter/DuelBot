from discord.ext import commands
from .command_invite import invite as command_invite
from .command_server import server as command_server
from .command_bot_highscores import hs as command_hs
from .command_refer import refer as command_refer


class MiscCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        await command_invite(ctx)

    @commands.command()
    async def server(self, ctx):
        await command_server(ctx)

    @commands.command()
    async def hs(self, ctx, *args):
        await command_hs(ctx, *args)

    @commands.command()
    async def refer(self, ctx, referral_user):
        await command_refer(ctx, referral_user)


def setup(bot):
    bot.add_cog(MiscCommands(bot))
