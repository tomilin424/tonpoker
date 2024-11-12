import asyncio
import json
import logging
from websockets.server import serve
from typing import Dict, Set
from game.poker_game import PokerGame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokerWebSocketServer:
    def __init__(self):
        self.clients: Dict[int, Set] = {}  # tournament_id -> set of websockets
        self.games: Dict[int, PokerGame] = {}  # tournament_id -> game
    
    async def register(self, websocket, tournament_id: int):
        """Регистрирует нового клиента"""
        if tournament_id not in self.clients:
            self.clients[tournament_id] = set()
        self.clients[tournament_id].add(websocket)
        logger.info(f"Client connected to tournament {tournament_id}")
    
    async def unregister(self, websocket, tournament_id: int):
        """Удаляет клиента"""
        self.clients[tournament_id].remove(websocket)
        logger.info(f"Client disconnected from tournament {tournament_id}")
    
    async def broadcast(self, tournament_id: int, message: dict):
        """Отправляет сообщение всем клиентам турнира"""
        if tournament_id in self.clients:
            websockets = self.clients[tournament_id]
            if websockets:
                await asyncio.gather(
                    *[ws.send(json.dumps(message)) for ws in websockets]
                )
    
    async def handle_connection(self, websocket):
        """Обрабатывает WebSocket соединение"""
        try:
            # Получаем ID турнира при подключении
            async for message in websocket:
                data = json.loads(message)
                tournament_id = data.get('tournament_id')
                
                if not tournament_id:
                    continue
                
                # Регистрируем клиента
                await self.register(websocket, tournament_id)
                
                # Обрабатываем действия игрока
                if 'action' in data:
                    game = self.games.get(tournament_id)
                    if game:
                        result = await game.handle_action(
                            data['user_id'],
                            data['action'],
                            data.get('amount')
                        )
                        # Отправляем обновление всем игрокам
                        await self.broadcast(tournament_id, result)
        
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
        finally:
            await self.unregister(websocket, tournament_id)
    
    async def start_server(self, host: str = 'localhost', port: int = 8765):
        """Запускает WebSocket сервер"""
        async with serve(self.handle_connection, host, port):
            logger.info(f"WebSocket server started on ws://{host}:{port}")
            await asyncio.Future()  # run forever 