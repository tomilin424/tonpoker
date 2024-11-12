from typing import Dict, List
from datetime import datetime
import random

class Tournament:
    def __init__(self, tournament_id: str, tournament_type: str, buy_in: float, max_players: int):
        self.id = tournament_id
        self.type = tournament_type
        self.buy_in = buy_in
        self.max_players = max_players
        self.players = []
        self.status = 'registering'  # registering, running, completed
        self.prize_pool = 0
        self.start_time = None
        self.end_time = None
        
        # Настройки турнира
        self.starting_chips = buy_in * 100
        self.blind_levels = [
            {'small': 10, 'big': 20, 'ante': 0, 'duration': 300},
            {'small': 15, 'big': 30, 'ante': 5, 'duration': 300},
            {'small': 25, 'big': 50, 'ante': 5, 'duration': 300},
            {'small': 50, 'big': 100, 'ante': 10, 'duration': 300},
            {'small': 75, 'big': 150, 'ante': 15, 'duration': 300},
        ]
        self.current_level = 0
    
    def add_player(self, user_id: int, username: str) -> Dict:
        """Добавляет игрока в турнир"""
        if len(self.players) >= self.max_players:
            return {'status': 'error', 'message': 'Турнир уже заполнен'}
            
        if any(p['user_id'] == user_id for p in self.players):
            return {'status': 'error', 'message': 'Вы уже зарегистрированы'}
            
        self.players.append({
            'user_id': user_id,
            'username': username,
            'chips': self.starting_chips,
            'status': 'active',
            'position': None
        })
        
        self.prize_pool += self.buy_in
        
        # Если турнир заполнен, меняем статус
        if len(self.players) >= self.max_players:
            self.status = 'starting'
            self.start_time = datetime.now()
        
        return {'status': 'success'}
    
    def get_current_blinds(self) -> Dict:
        """Возвращает текущие блайнды"""
        return self.blind_levels[self.current_level]
    
    def increase_blinds(self) -> bool:
        """Увеличивает уровень блайндов"""
        if self.current_level < len(self.blind_levels) - 1:
            self.current_level += 1
            return True
        return False 