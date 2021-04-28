class DuelUser:
    hitpoints = 99
    special = 100
    poisoned = False
    lastAttack = None
    user = None

    def __init__(self, user):
        self.user = user

        if user.nick == None:
            user.nick = user.name


class Duel:
    user_1 = None
    user_2 = None
    turn = None
    turnCount = 0
    uuid = None
    stakeItem = None

    def __init__(self, user, uuid, channel):
        self.user_1 = user
        self.uuid = uuid,
        self.channel = channel
