from cogs.dueling.create_duel import create_duel
import globals


async def fight(message, *args):
    await create_duel(message, args)

    channel_duel = globals.duels.get(message.channel.id, None)

    if channel_duel is None:
        return
