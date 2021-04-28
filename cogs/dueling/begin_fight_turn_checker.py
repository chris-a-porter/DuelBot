import globals
import asyncio
from .update_db_with_duel_results import update_db_with_duel_results

async def beginFightTurnChecker(message, duel):
    channelDuel = globals.duels.get(message.channel.id, None)

    # switches who's turn it is
    savedTurn = channelDuel.turn

    attackTypes = ["=dds",
                   "=ags",
                   "=sgs",
                   "=dclaws",
                   "=whip",
                   "=elder",
                   "=zgs",
                   "=dlong",
                   "=dmace",
                   "=dwh",
                   "=ss",
                   "=gmaul",
                   "=ice",
                   "=blood",
                   "=smoke",
                   "=bp"]

    def checkParameters(message):
        channelDuel = globals.duels.get(message.channel.id, None)
        attackTypes = ["=dds",
                       "=ags",
                       "=sgs",
                       "=dclaws",
                       "=whip",
                       "=elder",
                       "=zgs",
                       "=dlong",
                       "=dmace",
                       "=dwh",
                       "=ss",
                       "=gmaul",
                       "=ice",
                       "=blood",
                       "=smoke",
                       "=bp"]

        attackTypeCheck = None

        if message.content in attackTypes:
            attackTypeCheck = True
        else:
            attackTypeCheck = False

        return channelDuel != None and message.author.id == savedTurn.user.id and attackTypeCheck == True and duel.turnCount == \
               globals.duels[message.channel.id].turnCount

    try:
        msg = await globals.bot.wait_for('message', check=checkParameters, timeout=180)

    except asyncio.TimeoutError:
        # called when it times out

        turnUser = None
        notTurn = None

        channelDuel = globals.duels.get(message.channel.id, None)

        if channelDuel == None:
            return

        if channelDuel.turn.user.id == channelDuel.user_1.user.id and channelDuel.uuid == duel.uuid:
            turnUser = channelDuel.user_1
            notTurn = channelDuel.user_2
        elif channelDuel.uuid == duel.uuid and channelDuel.turnCount == duel.turnCount:
            turnUser = channelDuel.user_2
            notTurn = channelDuel.user_1
        await message.channel.send(
            f'The duel ran too long and has been timed out. Duels can only last a a maximum of three minutes.')
        globals.duels[message.channel.id] = None