import discord


async def fight_commands(self, message):
    embed = discord.Embed(title="Duel bot commands", color=discord.Color.orange())
    embed.add_field(name="Server commands",
                    value="**=server**: Links to our server. Members get +1 loot roll for pking and fighting!\n"
                          "**=invite**: Gives an invite link to add the DuelBot to your server.", inline=False)
    embed.add_field(name="General commands", value="**=fight**: Begins a duel \n"
                                                   "**=kd**: View your kill/death ratio \n"
                                                   "**=rares**: See all of the rares you've won \n"
                                                   "**=gp**: See how much GP you have", inline=False)
    embed.add_field(name="Fighting commands",
                    value="**=dds**: Hits twice, max of **18** each hit, uses 25% special, 25% chance to poison \n"
                          "**=whip**: Hits once, max of **27** \n"
                          "**=elder**: Hits once, max of **35** \n"
                          "**=ags**: Hits once, max of **46**, uses 50% of special \n"
                          "**=sgs**: Hits once, max of **39**, uses 50% of special, heals for 50% of damage \n"
                          "**=zgs**: Hits once, max of **36**, uses 50% of special, has a 25% chance to freeze enemy \n"
                          "**=dclaws**: Hits four times, max of **21** on any hit, each consecutive hit does 50% damage \n"
                          "**=dwh**: Hits once, max of **39**, uses 50% special \n"
                          "**=ss**: Hits twice, max of **27** each hit, uses 100% special \n"
                          "**=gmaul**: Hits three times, max of **24** each hit, uses 100% special \n"
                          "**=bp**: Hits once, max of **27**, uses 50% special, heals for 50% of damage, 25% chance to poison \n"
                          "**=ice**: Hits once, max of **30**, has a 12.5% chance to freeze enemy\n"
                          "**=blood**: Hits once, max of **28**, heals for 25% of damage \n"
                          "**=smoke**: Hits once, max of **27**, 25% chance to poison"
                    , inline=False)
    await message.send(embed=embed)
