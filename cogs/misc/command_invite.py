# Display a lasting invite to bring a bot into your server


async def invite(ctx):
    await ctx.send("""
    Click the link below to add the DuelBot to your server! \n
    https://discordapp.com/api/oauth2/authorize?client_id=684592148284571670&permissions=388160&scope=bot
    """)