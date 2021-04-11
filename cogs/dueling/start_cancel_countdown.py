import asyncio


async def start_cancel_countdown(message, saved_uuid):

    await asyncio.sleep(60.0)

    channel_duel = globals.duels.get(message.channel.id, None)

    if channel_duel is None:
        return

    if channel_duel.user_2 is None and channel_duel.uuid == saved_uuid:
        del globals.duels[message.channel.id]
        await message.send("Nobody accepted the duel.")

    elif channel_duel.user_2 is not None:
        return
