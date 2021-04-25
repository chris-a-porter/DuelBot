from osrsbox import items_api

def init():
    global duels
    duels = {}
    global lastMessages
    lastMessages = {}
    global all_db_items
    all_db_items = items_api.load()