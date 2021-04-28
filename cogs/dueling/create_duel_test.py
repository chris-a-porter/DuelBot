from helpers.math_helpers import numify, short_numify
from ..economy.store.get_number_of_item_owned_by_player import get_number_of_item_owned_by_player
from ..economy.bank.remove_item_from_user import remove_item_from_user
import uuid
from rs_api.get_item_name import get_item_name
import random
from ..item_files.rares import rare_items
from ..item_files.lootable_pk_items import pk_items
import globals

async def createDuel(self, message, *args):
    async def convertArgsToItemString(args):

        itemName = ""
        itemQuantity = 0
        try:
            try:
                # Test if the argument is an integer
                itemQuantity = int(args[0])
            except:
                # Test if the argument is a string
                try:
                    placeholderQuantity = int(numify(args[0]))
                    if type(placeholderQuantity) == int:
                        itemQuantity = placeholderQuantity
                except:
                    itemQuantity = None
            # If the first argument is an integer,
            if type(itemQuantity) != int:
                await message.send('Please enter a valid quantity.')
                return None
        except Exception as e:
            await message.send('Please enter a quantity to stake.')
            return None

        if len(args) == 1:  # If the user didn't include an item to purchase, but did include a quantity (is staking GP)
            itemName = "GP"
        elif len(args) == 2:  # If the args was two values long, including an integer
            itemName = args[1]
        else:  # If the args was more than two words long, concatenate
            for n in range(1, len(args)):
                itemName += args[n]

        # Cast the itemName to its lowercase version
        itemName = itemName.lower()
        # Return [name of item, quantity to stake]
        return [itemName, itemQuantity]

    def get_key(val, itemDict):
        for key, value in itemDict.items():
            if val == value:
                return key
        return None

    async def getStakeType():
        stakeType = ""
        arguments = args[0]
        itemLongName = ""
        itemId = None

        if len(arguments) == 0:
            return None
        # If there is only one argument
        if len(arguments) == 1:
            # Try to convert the argument into a number, because the stake should be GP
            value = numify(arguments[0])
            try:
                # If the number did not successfully convert to a number, this will throw an exception when int(value) is called
                # If it is successful, it will return "gp" to indicate a monetary stake
                intValue = int(value)
                stakeType = "gp"
                return [stakeType, arguments[0]]
            except:
                return None

        # If there are two arguments (could be "[quantity] [text]" or "[text] [text]")
        if len(arguments) == 2 or len(arguments) == 3:
            try:
                # Try to convert the arguments into a a [name, quantity] array
                # This will fail if the
                stakeVals = await convertArgsToItemString(arguments)
                if stakeVals == None:
                    return

                # Check to see if the name of the item is in either of the item dictionaries
                if stakeVals[0] in rare_items.keys():
                    stakeType = "rares"
                    itemLongName = rare_items[stakeVals[0]][2]
                    itemId = rare_items[stakeVals[0]][0]
                    return [stakeType, itemLongName, itemId]
                elif stakeVals[0] in pk_items.values():
                    stakeType = "items"
                    itemId = get_key(stakeVals[0], pk_items)
                    itemLongName = get_item_name(itemId)
                    return [stakeType, itemLongName, itemId]
                else:
                    await message.send("Couldn't find that item, please try again.")
                    return
            except:
                await message.send("Couldn't find that item, please try again.")
                return
        else:
            await message.send("Something went wrong.")
            return None

    # Returns [stake type, full name, itemId]
    # Stake type can be 'items', 'rares', or 'gp'
    # i.e. ['rares', 'Christmas cracker', 962]
    stakeType = await getStakeType()

    # Get the item quantity and itemName for the stake
    # Returned as [itemName, itemQuantity]
    # i.e. ['christmasCracker', 1]
    stakeParams = None
    if stakeType == None:
        # If the duel is just a regular old duel
        stakeParams = [None, None]
    else:
        stakeParams = await convertArgsToItemString(args[0])

    # Get the global duel
    channelDuel = globals.duels.get(message.channel.id, None)

    # Determine if the user has enough of the item
    async def checkUsersItemQuantity(user):

        if channelDuel != None and stakeParams[1] == None:
            if channelDuel.stakeItem == 'gp':
                await message.send(f"You don't have {channelDuel.shortQuantity} GP to stake.")
            else:
                if len(args[0]) == 0:
                    return True
                else:
                    if stakeParams[0] != channelDuel.itemLongName.replace(' ', '').lower():
                        await message.send(
                            f'Please type **=fight {channelDuel.shortQuantity} {channelDuel.itemLongName}** to enter this duel.')
                    elif stakeParams[0] == channelDuel.itemLongName.replace(' ', '').lower():
                        await message.send(
                            f"You don't have {channelDuel.shortQuantity} {channelDuel.itemLongName} to stake.")
            return False

        # Sort out values
        _itemType = stakeType[0]
        _fullItemName = stakeType[1]
        _itemId = None
        _shortItemName = stakeParams[0]
        _itemQuantity = stakeParams[1]
        _table = None

        if _itemType == 'gp':
            _table = 'duel_users'
            _itemId = 'gp'
        elif _itemType == 'rares':
            _table = 'duel_rares'
            _itemId = f"_{stakeType[2]}"
        elif _itemType == 'items':
            _table = 'pking_items'
            _itemId = f"_{stakeType[2]}"

        _userQuantity = await get_number_of_item_owned_by_player(user.id, _table, f"{_itemId}")

        if _userQuantity < _itemQuantity:
            if _itemType == 'gp':
                if message.author.id == user.id:
                    await message.send(f"You don't have {_shortItemName} to stake.")
                else:
                    await message.send(f"{user.id} does not {_shortItemName} to stake.")
            else:
                shortQuantity = short_numify(_itemQuantity, 1)

                if message.author.id == user.id:
                    await message.send(f"You don't have {shortQuantity} {_fullItemName} to stake.")
                else:
                    await message.send(f"{user.id} does not have {shortQuantity} {_fullItemName} to stake")
            return False
        elif _userQuantity >= _itemQuantity:
            return True

    if len(args[0]) != 0:
        user1HasItem = await checkUsersItemQuantity(message.author)

        if user1HasItem == False:
            return

    # Returns an array that details
    # where the user should have their info pulled to/written to
    # i.e. ['gp', 'duel_users'] or ['_1040', 'duel_rares']
    def returnTableColumn():
        # Sort out values
        _itemType = None
        if stakeType != None:
            _itemType = stakeType[0]
        _itemId = None
        _table = None

        if _itemType == 'gp':
            _table = 'duel_users'
            _itemId = 'gp'
        elif _itemType == 'rares':
            _table = 'duel_rares'
            _itemId = f"_{stakeType[2]}"
        elif _itemType == 'items':
            _table = 'pking_items'
            _itemId = f"_{stakeType[2]}"

        return [_itemId, _table]

    if channelDuel != None:
        if len(args[0]) > 0:
            if str(args[0][0]).lower() != str(channelDuel.shortQuantity).lower() and channelDuel.stakeItem == 'gp':
                await message.send(f'Please type **=fight {channelDuel.shortQuantity}** to enter this duel.')
                return
            elif str(args[0][0]).lower() != str(channelDuel.shortQuantity).lower() and channelDuel.stakeItem != 'gp' and \
                    stakeParams[0] != channelDuel.itemLongName.replace(' ', '').lower():
                await message.send(
                    f'Please type **=fight {channelDuel.shortQuantity} {channelDuel.itemLongName}** to enter this duel.')
                return
            else:
                pass

        if channelDuel.stakeItem != None:
            userHasQuantity = await checkUsersItemQuantity(message.author)

            if userHasQuantity == False:
                return

    # Check to see if a duel exists in the channel
    if channelDuel == None:
        if len(args[0]) == 0:
            # If the duel is not for any particular amount of money
            globals.duels[message.channel.id] = globals.Duel(globals.DuelUser(message.author), uuid.uuid4(),
                                                             message.channel.id, None, None, None, None, None)
            channelDuel = globals.duels.get(message.channel.id, None)
            globals.lastMessages[message.channel.id] = await message.send(
                f"<@{message.author.id}> has started a duel. Type **=fight** to duel them.")
            await self.startCancelCountdown(message, channelDuel.uuid)
            return
        elif args != None:
            # If the stake has a value attached to it
            table = returnTableColumn()

            if stakeParams[1] < 0:
                await message.send("You cannot stake less than 1 of an item.")
                return

            globals.duels[message.channel.id] = globals.Duel(globals.DuelUser(message.author), uuid.uuid4(),
                                                             message.channel.id, table[0], stakeParams[1], table[1],
                                                             stakeType[1],
                                                             short_numify(stakeParams[1], 1))
            channelDuel = globals.duels.get(message.channel.id, None)
            if stakeType[0] == 'gp':
                globals.lastMessages[message.channel.id] = await message.send(
                    f"**<@{message.author.id}>** has started a duel for **{args[0][0]} GP**. Type **=fight {args[0][0]}** to duel them.")
            else:
                globals.lastMessages[message.channel.id] = await message.send(
                    f"**{message.author.id}** has started a duel for **{args[0][0]} {stakeType[1]}**. Type **=fight {short_numify(stakeParams[1], 1)} {stakeType[1]}** to duel them.")

            await self.startCancelCountdown(message, channelDuel.uuid)
            return
    else:
        if channelDuel.stakeItem != None:
            userHasQuantity = await checkUsersItemQuantity(message.author)

            if userHasQuantity == False:
                return

    # Check to see if the person is dueling themselves
    if self.check(message.author, message.channel.id) == False:
        await message.send("You cannot duel yourself.")
        return

    # Check to see if a duel already exists between two people
    if channelDuel.user_1 != None and channelDuel.user_2 != None:
        await message.send("There are already two people dueling.")
        return

    # Check to see if player 2 has the required items to participate in the stake
    player2HasQuantity = await checkUsersItemQuantity(message.author)
    if player2HasQuantity == False:
        return

    # # If it passed the other checks, add duel user 2 to the fight
    # channelDuel.user_2 = globals.DuelUser(message.author)

    if channelDuel.stakeItem != None and channelDuel.stakeQuantity != None:
        tableValues = returnTableColumn()

        if len(args[0]) == 0:
            await message.send(
                f'Please type **=fight {channelDuel.shortQuantity} {channelDuel.itemLongName}** to enter this duel.')
            return
        if stakeType[1].replace(' ', '').lower() == channelDuel.itemLongName.replace(' ', '').lower():
            player1HasQuantityStill = await checkUsersItemQuantity(channelDuel.user_1.user)
            if player1HasQuantityStill == False:
                await message.send(
                    f"Cancelling the duel because {channelDuel.user_1.user.id} no longer has {short_numify(stakeParams[1], 1)} {stakeType[1]}.")
                del globals.duels[message.channel.id]
                return
        elif stakeType[1].replace(' ', '').lower() != channelDuel.itemLongName.replace(' ', '').lower():
            await message.send(f"The current duel is not for {stakeType[1]}.")
            return

        # If it passed the other checks, add duel user 2 to the fight
        channelDuel.user_2 = globals.DuelUser(message.author)

        await remove_item_from_user(channelDuel.user_1.user.id, channelDuel.table, channelDuel.stakeItem,
                                                   channelDuel.stakeQuantity)
        await remove_item_from_user(channelDuel.user_2.user.id, channelDuel.table, channelDuel.stakeItem,
                                                   channelDuel.stakeQuantity)
    elif channelDuel.stakeItem == None:
        channelDuel.user_2 = globals.DuelUser(message.author)

    # Randomly pick a starting user
    startingUserBool = bool(random.getrandbits(1))
    startingUser = None
    if startingUserBool == True:
        startingUser = channelDuel.user_1
        channelDuel.turn = channelDuel.user_1
    else:
        startingUser = channelDuel.user_2
        channelDuel.turn = channelDuel.user_2

    try:
        del globals.lastMessages[message.channel.id]
    except:
        pass

    await message.send(
        f"Beginning duel between {channelDuel.user_1.user.id} and {channelDuel.user_2.user.id} \n**{startingUser.user.id}** goes first.")

    if channelDuel.user_1 != None and channelDuel.user_2 != None:
        await self.beginFightTurnChecker(message, channelDuel)