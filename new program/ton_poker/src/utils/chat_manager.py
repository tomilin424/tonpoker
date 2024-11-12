from typing import Dict, List
from datetime import datetime
import asyncio

class ChatManager:
    def __init__(self, bot):
        self.bot = bot
        self.chats = {}  # tournament_id -> messages
        self.max_messages = 100
    
    async def send_message(self, tournament_id: str, user_id: int, username: str, text: str):
        """Отправляет сообщение всем игрокам турнира"""
        if tournament_id not in self.chats:
            self.chats[tournament_id] = []
        
        message = {
            'user_id': user_id,
            'username': username,
            'text': text,
            'timestamp': datetime.now()
        }
        
        self.chats[tournament_id].append(message)
        
        # Ограничиваем историю сообщений
        if len(self.chats[tournament_id]) > self.max_messages:
            self.chats[tournament_id] = self.chats[tournament_id][-self.max_messages:]
        
        # Отправляем сообщение всем игрокам турнира
        tournament = self.bot.tournaments.get(tournament_id)
        if tournament:
            for player in tournament.players:
                if player['user_id'] != user_id:  # Не отправляем отправителю
                    try:
                        await self.bot.send_message(
                            player['user_id'],
                            f"💭 {username}: {text}"
                        )
                    except Exception as e:
                        print(f"Error sending message to {player['user_id']}: {e}") 