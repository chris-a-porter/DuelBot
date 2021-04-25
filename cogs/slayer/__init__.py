from discord.ext import commands
from .command_slay import command_slay
from .command_switch import switch
from .command_mystats import command_mystats
import math


class SlayerCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slay(self, ctx, *args):
        await command_slay(ctx, *args)
        return

    @commands.command()
    async def switch(self, ctx, style):
        await command_switch(ctx, style)
        return

    @switch.error
    async def switchError(self, ctx):
        await ctx.send(
            "Proper syntax is *=switch [style]* \nYou can currently train Attack, Strength, Defence, Ranged and Magic.")

    @commands.command()
    async def mystats(self, ctx):
        await command_mystats(ctx)
        return


    @commands.command()
    @commands.cooldown(1, 60 * 120, commands.BucketType.user)
    async def fc(self, ctx):
        return

    @fc.error
    async def fcError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You are already in the Fight Caves. There are {math.ceil(error.retry_after / 60)} minutes left in your attempt.")


def setup(bot):
    bot.add_cog(SlayerCommands(bot))
