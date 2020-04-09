import unittest
import aiohttp.web
import asyncio
from RPS.gameManager import GameManager

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

class gameManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_loop = MockLoop()
        self.mock_app = aiohttp.web.Application(loop=self.mock_loop)
        self.mock_game_manager = GameManager(self.mock_app)
        self.mock_ws1 = MockWebSocket()
        self.mock_ws2 = MockWebSocket()

    def test_gameManager_type(self):
        self.assertIsInstance(self.mock_game_manager, GameManager)

    @async_test
    async def test_gameManager_connectPlayer(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.assertIn(self.mock_ws1, self.mock_game_manager.players)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.assertIn(self.mock_ws2, self.mock_game_manager.players)

    @async_test
    async def test_gameManager_connectPlayer_with_same_usernames(self):
        player1 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.assertIn(self.mock_ws1, self.mock_game_manager.players)
        player2 = await self.mock_game_manager.connectPlayer('Alex', self.mock_ws2)
        self.assertEqual(player2, None)

    @async_test
    async def test_gameManager_disconnect_player_removed_from_playersDict(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.disconnect(self.mock_ws1)
        self.assertNotIn(self.mock_ws1, self.mock_game_manager.players)

    @async_test
    async def test_gameManager_playerQueue_adds_players(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.assertEqual(len(self.mock_game_manager.playerQueue),1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        self.assertEqual(len(self.mock_game_manager.playerQueue),2)

    @async_test
    async def test_gameManager_disconnectPlayer_emptyPlayerQueue(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        self.assertEqual(len(self.mock_game_manager.playerQueue),1)
        await self.mock_game_manager.disconnect(self.mock_ws1)
        self.assertEqual(len(self.mock_game_manager.playerQueue),0)

        
    @async_test
    async def test_gameManager_createGame_removes_from_player_queue(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        await self.mock_game_manager.createGame()
        self.assertEqual(len(self.mock_game_manager.playerQueue),0)
    
    @async_test
    async def test_gameManager_gamesDict(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        await self.mock_game_manager.createGame()
        self.assertEqual(len(self.mock_game_manager.games),2)

    @async_test
    async def test_gameManager_disconnect_erases_players_from_games(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        await self.mock_game_manager.createGame()
        await self.mock_game_manager.disconnect(self.mock_ws1)
        self.assertEqual(len(self.mock_game_manager.games),0)

    @async_test
    async def test_gameManager_disconnect_player_returns_to_queue(self):
        await self.mock_game_manager.connectPlayer('Alex', self.mock_ws1)
        await self.mock_game_manager.connectPlayer('Sasha', self.mock_ws2)
        await self.mock_game_manager.createGame()
        await self.mock_game_manager.disconnect(self.mock_ws1)
        self.assertEqual(len(self.mock_game_manager.playerQueue),1)

if __name__ == '__main__':
    unittest.main()