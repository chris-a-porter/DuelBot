import psycopg2
import os
import discord

DATABASE_URL = os.environ['DATABASE_URL']


async def mystats(self, ctx):
    await Skilling(self.bot).createSkillTable(ctx.author.id)

    combat = await Skilling(self.bot).getCombatLevel(ctx.author.id)
    attack = await Skilling(self.bot).getLevel(ctx.author.id, 'attack')
    strength = await Skilling(self.bot).getLevel(ctx.author.id, 'strength')
    defence = await Skilling(self.bot).getLevel(ctx.author.id, 'defence')
    hitpoints = await Skilling(self.bot).getLevel(ctx.author.id, 'hitpoints')
    ranged = await Skilling(self.bot).getLevel(ctx.author.id, 'ranged')
    magic = await Skilling(self.bot).getLevel(ctx.author.id, 'magic')
    herblore = await Skilling(self.bot).getLevel(ctx.author.id, 'herblore')
    prayer = await Skilling(self.bot).getLevel(ctx.author.id, 'prayer')
    slayer = await Skilling(self.bot).getLevel(ctx.author.id, 'slayer')

    skills_column_1 = f"""{ItemEmojis.Skills.hitpoints} {hitpoints}
    {ItemEmojis.Misc.combat} {combat}
    {ItemEmojis.Skills.attack} {attack}
    {ItemEmojis.Skills.strength} {strength}
    {ItemEmojis.Skills.defence} {defence}
    {ItemEmojis.Skills.ranged} {ranged}
    {ItemEmojis.Skills.magic} {magic}
    {ItemEmojis.Skills.prayer} {prayer}
    {ItemEmojis.Skills.herblore} {herblore}
    {ItemEmojis.Skills.slayer} {slayer}
    """

    embed = discord.Embed(title=f"DuelBot stats for {ctx.author.mention}", color=discord.Color.blurple())
    embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/8/8c/HiScores_icon.png?99743')
    embed.add_field(name="\u200b", value=skills_column_1)

    await ctx.send(embed=embed)