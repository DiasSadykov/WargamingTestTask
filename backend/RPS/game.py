from enum import Enum
import json

class State(Enum):
    STARTED = 1
    ENDED = 2

class Game(object):

    def __init__(self, player1, player2, app, playerQueue, games):
        self._state = State.ENDED
        self.app = app
        self.player1 = player1
        self.player2 = player2
        self.games = games
        self.playerQueue = playerQueue

    async def startGame(self):
        self.player1.action, self.player2.action = None, None
        await self.sendMessage(self.player1, json.dumps({'status':'game is started'}))
        await self.sendMessage(self.player2, json.dumps({'status':'game is started'}))

    async def stopGame(self):
        await self.sendMessage(self.player1, json.dumps({'status':'game is ended'}))
        await self.sendMessage(self.player2, json.dumps({'status':'game is ended'}))
        self.player1.ready, self.player2.ready = False, False
        self.playerQueue.append(self.player1)
        self.playerQueue.append(self.player2)
        self.player2.endGame()
        self.player2.endGame()
        del self.games[self.player1]
        del self.games[self.player2]

    async def sendMessage(self, player, msg):
        await player.ws.send_str(msg)

    def changeState(self, action):
        print(action, self._state)
        if action in ['Rock', 'Scissors','Paper'] and self._state == State.STARTED and self.player1.action and self.player2.action:
            print('move was seen')
            self._state = State.ENDED
            self.play()
        elif action == 'Ready' and self._state == State.ENDED and self.player1.ready and self.player2.ready:
            print('ya tut')
            self._state = State.STARTED
            self.app.loop.create_task(self.startGame())
        elif action == 'Stop':
            self._state = State.ENDED
            self.app.loop.create_task(self.stopGame())
        elif action == 'Timeout':
            self._state = State.ENDED
            self.timeout()

    def play(self):
        result = self.round()
        self.player1.endRound()
        self.player1.endRound()
        self.app.loop.create_task(self.sendMessage(self.player1,json.dumps(result)))
        self.app.loop.create_task(self.sendMessage(self.player2,json.dumps(result)))

    def round(self):
        if self.player1.action == self.player2.action:
            result = {"draw":True, "winner": None}
        else:
            winner = self.getWinner()
            result = {"draw":False, "winner": winner.name}
        result[self.player1.name] = self.player1.action
        result[self.player2.name] = self.player2.action
        result["status"] = "results"
        self.player1.action, self.player2.action = None, None
        self.player1.ready, self.player2.ready = False, False
        return result

    def getWinner(self):
        if self.player1.action == "Timeout": return self.player2
        if self.player2.action == "Timeout": return self.player1
        
        results = {('Paper','Rock') : self.player1,
            ('Paper','Scissors') : self.player2,
            ('Rock','Paper') : self.player2,
            ('Rock','Scissors') : self.player1,
            ('Scissors','Paper') : self.player1,
            ('Scissors','Rock') : self.player2}
        return results[(self.player1.action,self.player2.action)]

    def timeout(self):
        if self.player1.action == "Timeout" and self.player2.action == "Timeout":
           self.changeState('Stop')
        elif self.player1.action and self.player2.action :
            self.play()



            