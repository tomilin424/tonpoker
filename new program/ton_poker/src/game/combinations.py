from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Card:
    suit: str
    value: int
    
    def __str__(self):
        suits = {'♠': '♠', '♣': '♣', '♥': '♥', '♦': '♦'}
        values = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        return f"{values.get(self.value, str(self.value))}{suits[self.suit]}"

class HandEvaluator:
    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Dict:
        """Определяет комбинацию карт"""
        if HandEvaluator._is_royal_flush(cards):
            return {'rank': 10, 'name': 'Роял-флеш'}
        elif HandEvaluator._is_straight_flush(cards):
            return {'rank': 9, 'name': 'Стрит-флеш'}
        elif HandEvaluator._is_four_of_kind(cards):
            return {'rank': 8, 'name': 'Каре'}
        elif HandEvaluator._is_full_house(cards):
            return {'rank': 7, 'name': 'Фулл-хаус'}
        elif HandEvaluator._is_flush(cards):
            return {'rank': 6, 'name': 'Флеш'}
        elif HandEvaluator._is_straight(cards):
            return {'rank': 5, 'name': 'Стрит'}
        elif HandEvaluator._is_three_of_kind(cards):
            return {'rank': 4, 'name': 'Тройка'}
        elif HandEvaluator._is_two_pair(cards):
            return {'rank': 3, 'name': 'Две пары'}
        elif HandEvaluator._is_pair(cards):
            return {'rank': 2, 'name': 'Пара'}
        else:
            return {'rank': 1, 'name': 'Старшая карта'}
    
    @staticmethod
    def _is_royal_flush(cards: List[Card]) -> bool:
        if len(cards) < 5:
            return False
        
        for suit in ['♠', '♣', '♥', '♦']:
            suited_cards = [card for card in cards if card.suit == suit]
            if len(suited_cards) >= 5:
                values = sorted([card.value for card in suited_cards])
                if values[-5:] == [10, 11, 12, 13, 14]:
                    return True
        return False 