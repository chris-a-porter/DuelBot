from cogs.economy.economy import Bank


class User:

    def __init__(self, bot, user):
        self.bot = bot
        self.user = user
        self.bank = Bank(bot, user)


def setup(bot):
    bot.add_cog(User(bot))
