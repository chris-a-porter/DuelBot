# Checker function to see if a turn is taken in a set amount of time
import globals
import asyncio

async def turnChecker(message, duel):

    # Retrieve the duel for the channel
    channelDuel = globals.duels.get(message.channel.id, None)

    # Switches who's turn it is
    savedTurn = channelDuel.turn
    savedTurnCount = channelDuel.turnCount
    if channelDuel.turn == channelDuel.user_1:
        channelDuel.turn = channelDuel.user_2
    else:
        channelDuel.turn = channelDuel.user_1

    # Array of attack command strings
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

    # Nested discord 'check' function for checking to see if the duel has been altered
    def checkParameters(message):

        # Retrieve the duel for the channel
        channelDuel = globals.duels.get(message.channel.id, None)

        # Array of attack command strings
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

        # Does the content of the message pass the attack type check?
        # Sets attackTypeCheck to BOOL
        if message.content in attackTypes:
            attackTypeCheck = True
        else:
            attackTypeCheck = False

        # If there is no duel found, return
        if globals.duels.get(message.channel.id, None) == None:
            return

        # Return this executable to test if the duel has changed
        # If the duel exists (is not None) AND
        # If the author of the message sent is the same as the person who's turn it is AND
        # If the command used is one of the attack commands AND
        # If the duel has the same turn count as when initially called
        return channelDuel != None and message.author.id == savedTurn.user.id and attackTypeCheck == True and savedTurnCount == globals.duels[message.channel.id].turnCount

    try:
        # Wait for the person who's turn it is to send a messsage that matches the parameters in checkParameters(), executes after 90 seconds
        msg = await globals.bot.wait_for('message', check=checkParameters, timeout=90)

    except asyncio.TimeoutError:
        # Called when it times out

        # Placeholders for determining the user of the turn
        turnUser = None
        notTurn = None

        # Retrieve the duel for the channel
        channelDuel = globals.duels.get(message.channel.id, None)

        # If no duel exists, return ELSE IF
        # The turncount hasn't changed and the duel is the same duel from before (same uuid) THEN
        # Store the turnUser/notTurn variables for the last message
        if channelDuel == None:
            return
        elif channelDuel != None and channelDuel.turnCount == duel.turnCount and channelDuel.uuid == duel.uuid:
            if channelDuel.turn.user.id == channelDuel.user_1.user.id:
                turnUser = channelDuel.user_1
                notTurn = channelDuel.user_2
            else:
                turnUser = channelDuel.user_2
                notTurn = channelDuel.user_1

            # Send a message to the discord channel stating the winner and loser based on their nicknames in the channel
            await message.channel.send(f'{turnUser.user.id} took too long to take their turn. {notTurn.user.id} wins the duel.')

            # Log the timeout to the console, useful for debugging
            print(f'Duel in channel {message.channel.id} timed out.')

            # Delete the duel from the duels dict
            globals.duels[message.channel.id] = None