import asyncio
import aiohttp.web
import os
from .game import Game
from .player import Player
import json 
from collections import deque

class GameManager(object):
    def __init__(self, app):
        self.players = {}
        self.games = {}
        self.app = app
        self.playerQueue = deque()
        self.usernames = set()
        app.loop.create_task(self.matchPlayers())

    async def websocket_handler(self, request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                print(data)
                if data['message'] == 'connect':
                    await self.connectPlayer(data['name'], ws)
                elif data['message'] == 'action':
                    self.players[ws].takeAction(data['body'])
                elif data['message'] == 'disconnect':
                    await self.disconnect(ws)
        return ws


    async def matchPlayers(self):
        while True:
            await asyncio.sleep(0.1)
            if len(self.playerQueue) > 1:
                await self.createGame()

    async def createGame(self):
        player1 = self.playerQueue.popleft()
        player2 = self.playerQueue.popleft()
        game = Game(player1, player2, self.app, self.playerQueue, self.games)
        self.games[player1], self.games[player2] = game, game
        player1.setGame(game)
        player2.setGame(game)
        await player1.ws.send_str(json.dumps({'status': 'game is found', 'opponent': player2.name}))
        await player2.ws.send_str(json.dumps({'status': 'game is found', 'opponent': player1.name}))
        return game

    async def connectPlayer(self, name, ws):
        if name not in self.usernames:
            self.usernames.add(name)
            new_player = Player(name, ws)
            self.players[ws] = new_player
            self.playerQueue.append(new_player)
            await ws.send_str(json.dumps({'status':'you were connected'}))
            return new_player
        else:
            await ws.send_str(json.dumps({'status':'error','body':'username is taken, try another, please'}))
            return None

    async def disconnect(self, ws):
        if ws in self.players:
            playerToLeave = self.players[ws]
            if playerToLeave in self.games:
                gameToEnd = self.games[playerToLeave]
                await gameToEnd.stopGame()
            self.playerQueue.remove(playerToLeave)
            del self.players[ws]
            self.usernames.remove(playerToLeave.name)
            print(self.games)
            print(self.playerQueue)




