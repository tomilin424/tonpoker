from typing import Dict
import json
import os
from datetime import datetime

class PlayerStatistics:
    def __init__(self):
        self.stats = {}
        self.load_stats()
    
    def load_stats(self):
        """Загружает статистику из файла"""
        if os.path.exists('player_stats.json'):
            with open('player_stats.json', 'r') as f:
                self.stats = json.load(f)
    
    def save_stats(self):
        """Сохраняет статистику в файл"""
        with open('player_stats.json', 'w') as f:
            json.dump(self.stats, f)
    
    def update_stats(self, user_id: int, event_type: str, data: Dict):
        """Обновляет статистику игрока"""
        if str(user_id) not in self.stats:
            self.stats[str(user_id)] = {
                'games_played': 0,
                'tournaments_played': 0,
                'tournaments_won': 0,
                'total_winnings': 0,
                'best_hand': None,
                'biggest_pot': 0,
                'hands_played': 0,
                'hands_won': 0,
                'total_rake': 0,
                'last_game': None
            }
        
        player = self.stats[str(user_id)]
        
        if event_type == 'tournament_join':
            player['tournaments_played'] += 1
            player['last_game'] = datetime.now().isoformat()
        
        elif event_type == 'tournament_win':
            player['tournaments_won'] += 1
            player['total_winnings'] += data.get('prize', 0)
        
        elif event_type == 'hand_played':
            player['hands_played'] += 1
            if data.get('won', False):
                player['hands_won'] += 1
            
            pot_size = data.get('pot', 0)
            if pot_size > player['biggest_pot']:
                player['biggest_pot'] = pot_size
            
            if data.get('hand_rank', 0) > player.get('best_hand', {}).get('rank', 0):
                player['best_hand'] = {
                    'rank': data['hand_rank'],
                    'name': data['hand_name'],
                    'date': datetime.now().isoformat()
                }
        
        self.save_stats()
    
    def get_player_stats(self, user_id: int) -> Dict:
        """Возвращает статистику игрока"""
        return self.stats.get(str(user_id), {}) 