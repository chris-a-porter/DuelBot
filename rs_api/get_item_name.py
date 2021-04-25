import globals

# Returns the name of an item based on its ID


def get_item_name(item_id):
    for item in globals.all_db_items:
        if item.id == item_id:
            return item.name
