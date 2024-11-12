from typing import Dict, List
from datetime import datetime
import json

class Achievement:
    def __init__(self, id: str, name: str, description: str, reward: float, icon: str):
        self.id = id
        self.name = name
        self.description = description
        self.reward = reward
        self.icon = icon

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'first_game': Achievement(
                'first_game',
                '🎮 Первая игра',
                'Сыграйте свою первую игру',
                1.0,
                '🎮'
            ),
            'first_win': Achievement(
                'first_win',
                '🏆 Первая победа',
                'Выиграйте свой первый турнир',
                5.0,
                '🏆'
            ),
            'high_roller': Achievement(
                'high_roller',
                '💎 Хайроллер',
                'Сыграйте в турнире с бай-ином 100+ TON',
                10.0,
                '💎'
            ),
            'winning_streak': Achievement(
                'winning_streak',
                '🔥 Победная серия',
                'Выиграйте 3 турнира подряд',
                20.0,
                '🔥'
            ),
            'royal_flush': Achievement(
                'royal_flush',
                '👑 Роял-флеш',
                'Соберите роял-флеш',
                50.0,
                '👑'
            )
        }
        
        self.player_achievements = {}
        self.load_achievements()
    
    def load_achievements(self):
        try:
            with open('achievements.json', 'r') as f:
                self.player_achievements = json.load(f)
        except FileNotFoundError:
            pass
    
    def save_achievements(self):
        with open('achievements.json', 'w') as f:
            json.dump(self.player_achievements, f)
    
    def check_achievements(self, user_id: int, event: str, data: Dict) -> List[Achievement]:
        if str(user_id) not in self.player_achievements:
            self.player_achievements[str(user_id)] = []
        
        earned = []
        player_achievements = self.player_achievements[str(user_id)]
        
        if event == 'game_played':
            if 'first_game' not in player_achievements:
                earned.append(self.achievements['first_game'])
                player_achievements.append('first_game')
        
        elif event == 'tournament_win':
            if 'first_win' not in player_achievements:
                earned.append(self.achievements['first_win'])
                player_achievements.append('first_win')
            
            if data.get('buy_in', 0) >= 100 and 'high_roller' not in player_achievements:
                earned.append(self.achievements['high_roller'])
                player_achievements.append('high_roller')
        
        elif event == 'royal_flush' and 'royal_flush' not in player_achievements:
            earned.append(self.achievements['royal_flush'])
            player_achievements.append('royal_flush')
        
        if earned:
            self.save_achievements()
        
        return earned 