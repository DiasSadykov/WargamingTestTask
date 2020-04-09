import unittest
import aiohttp.web
import asyncio
from RPS.gameManager import GameManager
from RPS.game import Game
from RPS.game import State

def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper

class MockWebSocket():
    async def send_str(self,s):
        pass

class MockLoop():
    async def create_task(self,f):
        pass

class gameTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_loop = MockLoop()
        self.mock_app = aiohttp.web.Application(loop=self.mock_loop)
        self.mock_game_manager = GameManager(self.mock_app)
        self.mock_ws1 = MockWebSocket()
        self.mock_ws2 = MockWebSocket()

    @async_test
    async def test_game_type(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        game = await self.mock_game_manager.createGame()
        self.assertIsInstance(game, Game)

    @async_test
    async def test_game_not_ready(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.takeAction('Ready')
        self.assertNotEqual(self.mock_game._state, State.STARTED)

    @async_test
    async def test_game_ready(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.takeAction('Ready')
        self.mock_player2.takeAction('Ready')
        self.assertEqual(self.mock_game._state, State.STARTED)

    @async_test
    async def test_game_draw_true(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.takeAction('Ready')
        self.mock_player2.takeAction('Ready')
        self.mock_player1.action = 'Rock'
        self.mock_player2.action = 'Rock'
        result = self.mock_game.round()
        self.assertTrue(result['draw'])

    @async_test
    async def test_game_draw_false(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.takeAction('Ready')
        self.mock_player2.takeAction('Ready')
        self.mock_player1.action = 'Rock'
        self.mock_player2.action = 'Scissors'
        result = self.mock_game.round()
        self.assertFalse(result['draw'])

    @async_test
    async def test_game_winner(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.action = 'Rock'
        self.mock_player2.action = 'Scissors'
        result = self.mock_game.round()
        self.assertEqual(result['winner'], self.mock_player1.name)

    @async_test
    async def test_game_timeout_winner(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        self.mock_player1.action = 'Rock'
        self.mock_player2.action = 'Timeout'
        result = self.mock_game.round()
        self.assertEqual(result['winner'], self.mock_player1.name)
    
    @async_test
    async def test_game_stop_returns_players_to_queue(self):
        self.mock_player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.mock_player2 = await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.mock_game = await self.mock_game_manager.createGame()
        await self.mock_game.stopGame()
        self.assertEqual(len(self.mock_game_manager.playerQueue), 2)

