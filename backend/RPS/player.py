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
        """
        Handles players action and changes game state
        """
        if action == 'Ready':
            self.ready = True
        else:
            self.action = action
        self.game.changeState(action)

    def endRound(self):
        self.ready = False

    def endGame(self):
        """
        Detaches player from the game
        """
        self.game = None
        self.ready = False