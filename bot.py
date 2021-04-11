import discord
import os
import psycopg2
import uuid
import globals
globals.init()
from discord.ext import commands
import math
import asyncio
import random
from random import randint
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

bot = discord.ext.commands.Bot(command_prefix = '=')
duels = {}
lastMessages = {}
DATABASE_URL = os.environ['DATABASE_URL']

if __name__ == '__main__':
    print("booting up")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['DISCORD_KEY'])
