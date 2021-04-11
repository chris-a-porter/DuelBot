import math


async def sell(self, ctx, *args):
    def get_key(val, item_dict):
        for key, value in item_dict.items():
            if val == value:
                return key
        return None

    def get_full_item_name(item_id):
        for item in globals.all_db_items:
            if item.id == item_id:
                return item.name

    # Convert the arguments to a string usable for other searches
    async def convert_args_to_item_string(args):

        item_name_local = ""

        if len(args) == 1:  # If the user didn't include an item to purchase
            await ctx.send('Please enter a valid item.')
            return
        elif len(args) == 2:  # If the args was one word long
            item_name_local = args[1]
        elif len(args) == 3:  # If the args was two words long
            item_name_local = args[1] + args[2]
        else:  # If the args was more than two words long, default to two words to concatenate for the item to purchase
            for n in range(1, len(args)):
                item_name_local += args[n]

        return item_name_local

    async def convert_args_to_quantity(arg):
        # If the user does not enter a valid integer quantity of items to purchase
        try:
            item_quantity = int(arg)

            if item_quantity > 0:
                return item_quantity
            else:
                await ctx.send('You must sell at least one item.')
                return

        except TypeError:

            await ctx.send('Please enter a valid amount.')
            return

        except ValueError:

            await ctx.send('Proper syntax is *.buy [quantity] [item name].*')
            return

    # Create a table row for the user if it does not exist already
    await self.createPlayerItemTable(ctx.author.id)

    # Get the string of the items, formatted without spaces
    # i.e. redpartyhat

    item_name = await convert_args_to_item_string(args)

    # Get the quantity of the item, formatted as int
    item_quantity = await convert_args_to_quantity(args[0])

    # Find item in one of the dictionaries
    if item_name in self.rareIDs.keys():
        # If the item is a rare
        item_id = self.rareIDs[item_name][0]
        item_price = self.rareIDs[item_name][1]
        item_string = self.rareIDs[item_name][2]
        table = "duel_rares"
    elif item_name in self.itemList.values():
        # if the item is a regular item
        item_id = get_key(item_name, self.itemList)
        item_price = await self.getItemValue(item_id)
        item_string = get_full_item_name(item_id)
        table = "pking_items"
    else:
        await ctx.send("I don't buy that item.")
        return

    if item_price is None:
        await ctx.send("There was an error fetching the item price. Please try again.")
        return

    player_quantity = await self.getNumberOfItem(ctx.author.id, table, f"_{item_id}")

    if item_quantity > player_quantity:
        await ctx.send(f"You do not have {item_quantity}x {item_string} to sell.")
        return

    total_sale_price = math.floor(item_price * item_quantity * 0.8)
    comma_money = "{:,d}".format(total_sale_price)

    await self.removeItemFromUser(ctx.author.id, table, f"_{item_id}", item_quantity)
    await self.giveItemToUser(ctx.author.id, "duel_users", "gp", total_sale_price)
    await ctx.send(f"You have sold {item_quantity}x {item_string} for {comma_money} GP.")
    return
