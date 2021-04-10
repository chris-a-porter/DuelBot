import discord
from discord.ext import commands
from rs_api.get_rs_item_data import get_rs_item_data

class Store:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def items(self, ctx):
        return

    @commands.command()
    async def price(self, ctx):
        return

