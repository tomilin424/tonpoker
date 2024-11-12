from typing import Dict, List
from datetime import datetime

class ChatSystem:
    def __init__(self):
        self.messages = {}  # tournament_id -> [messages]
        self.max_messages = 100  # Максимальное количество сообщений в истории
    
    def add_message(self, tournament_id: str, user_id: int, username: str, text: str) -> Dict:
        """Добавляет сообщение в чат"""
        if tournament_id not in self.messages:
            self.messages[tournament_id] = []
            
        message = {
            'user_id': user_id,
            'username': username,
            'text': text,
            'timestamp': datetime.now().isoformat()
        }
        
        self.messages[tournament_id].append(message)
        
        # Ограничиваем историю сообщений
        if len(self.messages[tournament_id]) > self.max_messages:
            self.messages[tournament_id] = self.messages[tournament_id][-self.max_messages:]
            
        return message
    
    def get_messages(self, tournament_id: str, limit: int = 10) -> List[Dict]:
        """Возвращает последние сообщения из чата"""
        if tournament_id not in self.messages:
            return []
            
        return self.messages[tournament_id][-limit:] 