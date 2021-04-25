import random
import uuid
from cogs.dueling.classes import Duel, DuelUser
from cogs.dueling.duel_check import check
import globals

async def create_duel(message):

    global duels
    global lastMessages

    channel_duel = globals.duels.get(message.channel.id, None)

    if channel_duel == None:
        globals.duels[message.channel.id] = Duel(DuelUser(message.author), uuid.uuid4())
        channel_duel = globals.duels.get(message.channel.id, None)
        globals.lastMessages[message.channel.id] = await message.send(f"{message.author.nick} has started a duel. Type **.fight** to duel them.")
        return

    if check(message.author, message.channel.id) is False:
        await message.send("You cannot duel yourself.")
        return

    if channel_duel.user_1 != None and channel_duel.user_2 != None:
        await message.send("There are already two people dueling.")
        return

    channel_duel.user_2 = DuelUser(message.author)

    starting_user_bool = bool(random.getrandbits(1))

    starting_user = None

    if starting_user_bool is True:
        starting_user = channel_duel.user_1
        channel_duel.turn = channel_duel.user_1
    else:
        starting_user = channel_duel.user_2
        channel_duel.turn = channel_duel.user_2

    del globals.lastMessages[message.channel.id]
    await message.send(f"Beginning duel between {channel_duel.user_1.user.nick} and {channel_duel.user_2.user.nick} \n**{starting_user.user.nick}** goes first.")