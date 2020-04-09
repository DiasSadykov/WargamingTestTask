class Player(object):
    def __init__(self, name, ws):
        self.name = name
        self.ws = ws
        self.action = None
        self.game = None
        self.ready = False

    def setGame(self, game):
        self.game = game

    def takeAction(self, action):
        if action == 'Ready':
            self.ready = True
        else:
            self.action = action
        self.game.changeState(action)

    def endRound(self):
        self.ready = False

    def endGame(self):
        self.game = None
        self.ready = False