from osrsbox import items_api, monsters_api

def init(bot_client):

    global bot
    bot = bot_client

    global duels
    duels = {}

    global lastMessages
    lastMessages = {}

    global all_db_items
    all_db_items = items_api.load()

    global all_db_monsters
    all_db_monsters = monsters_api.load()

    global locations
    locations = {
        "wests": {
            "nicknames": [],
            "risk": 0.6,
            "uniques": [],
            "players": []
        },

        "easts": {
            "nicknames": [],
            "risk": 0.7,
            "uniques": [],
            "players": []
        },

        "mb": {
            "nicknames": [],
            "risk": 0.8,
            "uniques": [],
            "players": []
        },

        "edge": {
            "nicknames": [],
            "risk": 0.6,
            "uniques": [],
            "players": []
        },

        "lavas": {
            "nicknames": [],
            "risk": 0.9,
            "uniques": [],
            "players": []
        },

        "revs": {
            "nicknames": [],
            "risk": 1.0,
            "uniques": [21804, 21807, 21810, 21813, 21817, 22299, 22302, 22305, 4087, 4585, 22542, 22547, 22552],
            "players": []
        }

    }