import asyncio
import os
import discord
import psycopg2
import uuid
import random
from random import randint
from cogs.osrsEmojis import ItemEmojis
from cogs.loots import PotentialItems
import globals
from cogs.skilling.skilling import Skilling
from helpers.math_helpers import RSMathHelpers
from cogs.economy.economy import Economy
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']

class UserCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready')

    @commands.command()
    async def invite(self, ctx):
        return

    @commands.command()
    async def server(self, ctx):
        return

    # begin a duel command
    @commands.command()
    async def fight(self, message, *args):
        return

    @commands.command(name='commands')
    async def cmds(self, message):
        return

    @commands.command()
    async def rares(self, message):

    @commands.command()
    async def kd(self, message):
        return

    @commands.command()
    async def gp(self, message):
        return

    @commands.command()
    async def dice(self, message, *args):
        return

    @commands.command()
    async def hs(self, ctx, *args):
        return

    @commands.command()
    @commands.is_owner()
    async def givegp(self, ctx, *args):
        return

    @commands.command()
    async def pay(self, ctx, *args):
        return

def setup(bot):
    bot.add_cog(UserCommands(bot))
