import psycopg2
import os
import discord
from ..skilling.get_level import get_level
from ..skilling.get_combat_level import get_combat_level
from cogs.item_files.emojis_list import skills, misc_items

DATABASE_URL = os.environ['DATABASE_URL']


async def command_mystats(ctx):

    combat = await get_combat_level(ctx.author.id)
    attack = await get_level(ctx.author.id, 'attack')
    strength = await get_level(ctx.author.id, 'strength')
    defence = await get_level(ctx.author.id, 'defence')
    hitpoints = await get_level(ctx.author.id, 'hitpoints')
    ranged = await get_level(ctx.author.id, 'ranged')
    magic = await get_level(ctx.author.id, 'magic')
    herblore = await get_level(ctx.author.id, 'herblore')
    prayer = await get_level(ctx.author.id, 'prayer')
    slayer = await get_level(ctx.author.id, 'slayer')

    skills_column_1 = f"""{skills['hitpoints']} {hitpoints}
    {misc_items['combat]']} {combat}
    {skills['attack']} {attack}
    {skills['strength']} {strength}
    {skills['defence']} {defence}
    {skills['ranged']} {ranged}
    {skills['magic']} {magic}
    {skills['prayer']} {prayer}
    {skills['herblore']} {herblore}
    {skills['slayer']} {slayer}
    """

    embed = discord.Embed(title=f"DuelBot stats for {ctx.author.mention}", color=discord.Color.blurple())
    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/8/8c/HiScores_icon.png?99743')
    embed.add_field(name="\u200b", value=skills_column_1)

    await ctx.send(embed=embed)