import discord
import globals

async def scry(ctx):
    player_count_array = []
    for location in globals.locations.values():
        player_count_array.append(len(location['players']))

    embed = discord.Embed(title='You gaze into your scrying orb and see...', color=discord.Color.greyple())
    description = f""" Wests: {player_count_array[0]} players
    Easts: {player_count_array[1]} players
    Mage bank: {player_count_array[2]} players
    Edgeville: {player_count_array[3]} players
    Lava dragon isle: {player_count_array[4]} players
    Revenant caves: {player_count_array[5]} players 
    """
    embed.add_field(name="\u200b", value=description)
    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/d/db/Harmonised_orb.png?0ed98')
    await ctx.send(embed=embed)