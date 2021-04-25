import discord
from discord.ext import commands
import os
import globals
globals.init()


bot = commands.Bot(command_prefix = os.environ['PREFIX'])
duels = {}
lastMessages = {}
DATABASE_URL = os.environ['DATABASE_URL']

if __name__ == '__main__':
    print("DuelBot is booting up.")

bot.load_extension('cogs.admin')
bot.load_extension('cogs.dueling')
bot.load_extension('cogs.activities')
bot.load_extension('cogs.economy')
bot.load_extension('cogs.skilling')
bot.load_extension('cogs.misc')
bot.load_extension('cogs.lottery')
bot.load_extension('cogs.slayer')

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['DISCORD_KEY'])
