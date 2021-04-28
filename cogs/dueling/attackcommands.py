import os
from discord.ext import commands
from cogs.dueling.special_attacks.dragon_claws import dragon_claws_attack
from .freeze_attack import freezeAttack
from .special_attacks.dragon_claws import dragon_claws_attack
from .use_attack import use_attack

DATABASE_URL = os.environ['DATABASE_URL']

class AttackCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Weapon commands

    @commands.command()
    async def tickle(self, message):
        await use_attack(message, "tickly fingers", 0, 1, 1, 0, 0)

    @commands.command()
    async def dds(self, message):
        await use_attack(message, "DDS", 25, 2, 18, 0, True)

    @commands.command()
    async def whip(self, message):
        await use_attack(message, "Abyssal whip", 0, 1, 27, 0, False)

    @commands.command()
    async def ags(self, message):
        await use_attack(message, "Armadyl godsword", 50, 1, 46, 0, False)

    @commands.command()
    async def zgs(self, message):
        await freezeAttack(message, "Zamorak godsword", 50, 1, 36, 25)

    @commands.command()
    async def dlong(self, message):
        await use_attack(message, "Dragon longsword", 25, 1, 26, 0, False)

    @commands.command()
    async def dmace(self, message):
        await use_attack(message, "Dragon mace", 25, 1, 30, 0, False)

    @commands.command()
    async def dwh(self, message):
        await use_attack(message, "Dragon warhammer", 50, 1, 39, 0, False)

    @commands.command()
    async def ss(self, message):
        await use_attack(message, "Saradomin sword", 100, 2, 27, 0, False)

    @commands.command()
    async def gmaul(self, message):
        await use_attack(message, "Granite maul", 100, 3, 24, 0, False)

    @commands.command()
    async def ice(self, message):
        await use_attack(message, "Ice barrage", 0, 1, 30, 12.5)

    @commands.command()
    async def sgs(self, message):
        await use_attack(message, "Saradomin godsword", 50, 1, 37, 50, False)

    @commands.command()
    async def elder(self, message):
        await use_attack(message, "Elder Maul", 0, 1, 35, 0, False)

    @commands.command()
    # @commands.is_owner()
    async def dclaws(self, message):
        await dragon_claws_attack(message)

    @commands.command()
    async def bp(self, message):
        await use_attack(message, "Toxic blowpipe", 50, 1, 27, 50, False)

    @commands.command()
    async def blood(self, message):
        await use_attack(message, "Blood barrage", 0, 1, 29, 25, False)

    @commands.command()
    async def smoke(self, message):
        await use_attack(message, "Smoke barrage", 0, 1, 27, 0, True)


def setup(bot):
    bot.add_cog(AttackCommands(bot))
