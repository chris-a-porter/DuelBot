import discord
import os
import math
from cogs.loots import PotentialItems
from cogs.economy import Economy
from random import randint
import globals
from discord.ext import commands
from cogs.dueling.special_attacks.dragon_claws import dragon_claws_attack

DATABASE_URL = os.environ['DATABASE_URL']

class AttackCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Weapon commands
    # All non-freezing spells pull from 'useAttack()'
    # Freezing spells pull from 'freezeAttack()'
    # Dragon claws are currently an owner-only command
    # self.useAttack(message, name(string), %special(int), # damage rolls(int), max hit(int), %heal(int), poison(boolean))
    @commands.command()
    async def tickle(self, message):
        await self.useAttack(message, "tickly fingers", 0, 1, 1, 0, 0)

    @commands.command()
    async def dds(self, message):
        await self.useAttack(message, "DDS", 25, 2, 18, 0, True)

    @commands.command()
    async def whip(self, message):
        await self.useAttack(message, "Abyssal whip", 0, 1, 27, 0, False)

    @commands.command()
    async def ags(self, message):
        await self.useAttack(message, "Armadyl godsword", 50, 1, 46, 0, False)

    @commands.command()
    async def zgs(self, message):
        await self.freezeAttack(message, "Zamorak godsword", 50, 1, 36, 25)

    @commands.command()
    async def dlong(self, message):
        await self.useAttack(message, "Dragon longsword", 25, 1, 26, 0, False)

    @commands.command()
    async def dmace(self, message):
        await self.useAttack(message, "Dragon mace", 25, 1, 30, 0, False)

    @commands.command()
    async def dwh(self, message):
        await self.useAttack(message, "Dragon warhammer", 50, 1, 39, 0, False)

    @commands.command()
    async def ss(self, message):
        await self.useAttack(message, "Saradomin sword", 100, 2, 27, 0, False)

    @commands.command()
    async def gmaul(self, message):
        await self.useAttack(message, "Granite maul", 100, 3, 24, 0, False)

    @commands.command()
    async def ice(self, message):
        await self.freezeAttack(message, "Ice barrage", 0, 1, 30, 12.5)

    @commands.command()
    async def sgs(self, message):
        await self.useAttack(message, "Saradomin godsword", 50, 1, 37, 50, False)

    @commands.command()
    async def elder(self, message):
        await self.useAttack(message, "Elder Maul", 0, 1, 35, 0, False)

    @commands.command()
    # @commands.is_owner()
    async def dclaws(self, message):
        await dragon_claws_attack(self, message)

    @commands.command()
    async def bp(self, message):
        await self.useAttack(message, "Toxic blowpipe", 50, 1, 27, 50, False)

    @commands.command()
    async def blood(self, message):
        await self.useAttack(message, "Blood barrage", 0, 1, 29, 25, False)

    @commands.command()
    async def smoke(self, message):
        await self.useAttack(message, "Smoke barrage", 0, 1, 27, 0, True)


def setup(bot):
    bot.add_cog(AttackCommands(bot))
