import globals

def check(user, channel_id):

    channel_duel = globals.duels.get(channel_id, None)

    if channel_duel is None:
        print("This shouldn't ever call from check")

    return user != channel_duel.user_1.user
