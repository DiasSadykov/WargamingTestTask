import asyncio
import aiohttp.web
import os
from RPS.gameManager import GameManager

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


def run_server():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    gameManager = GameManager(app)
    app.router.add_route('GET', '/ws', gameManager.websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)

if __name__ == '__main__':
    run_server()






    
