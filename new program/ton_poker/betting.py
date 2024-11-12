from typing import Dict, List
from dataclasses import dataclass

@dataclass
class BettingRound:
    small_blind: int
    big_blind: int
    ante: int = 0
    min_raise: int = 0

class BettingManager:
    def __init__(self):
        self.blind_levels = [
            BettingRound(10, 20),
            BettingRound(15, 30, 5),
            BettingRound(25, 50, 5),
            BettingRound(50, 100, 10),
            BettingRound(75, 150, 15),
            BettingRound(100, 200, 25),
            BettingRound(150, 300, 30),
            BettingRound(200, 400, 50),
        ]
        self.current_level = 0
        
    def get_current_blinds(self) -> BettingRound:
        return self.blind_levels[self.current_level]
    
    def increase_blinds(self) -> bool:
        if self.current_level < len(self.blind_levels) - 1:
            self.current_level += 1
            return True
        return False
    
    def calculate_min_raise(self, current_bet: int) -> int:
        blinds = self.get_current_blinds()
        return max(blinds.big_blind, current_bet * 2)
    
    def get_possible_bets(self, player_chips: int, current_bet: int) -> List[int]:
        min_raise = self.calculate_min_raise(current_bet)
        possible_bets = []
        
        for multiplier in [1, 1.5, 2, 3]:
            bet = int(min_raise * multiplier)
            if bet <= player_chips:
                possible_bets.append(bet)
        
        # Добавляем олл-ин
        if player_chips > 0 and player_chips not in possible_bets:
            possible_bets.append(player_chips)
            
        return possible_bets 