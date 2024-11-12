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

class PokerHand:
    def __init__(self, cards: List[Card]):
        self.cards = sorted(cards, key=lambda x: x.value, reverse=True)
        self.rank = 0
        self.name = ""
        self.evaluate()
    
    def evaluate(self):
        """Определяет комбинацию карт"""
        if self._is_royal_flush():
            self.rank = 10
            self.name = "Роял-флеш"
        elif self._is_straight_flush():
            self.rank = 9
            self.name = "Стрит-флеш"
        elif self._is_four_of_kind():
            self.rank = 8
            self.name = "Каре"
        elif self._is_full_house():
            self.rank = 7
            self.name = "Фулл-хаус"
        elif self._is_flush():
            self.rank = 6
            self.name = "Флеш"
        elif self._is_straight():
            self.rank = 5
            self.name = "Стрит"
        elif self._is_three_of_kind():
            self.rank = 4
            self.name = "Тройка"
        elif self._is_two_pair():
            self.rank = 3
            self.name = "Две пары"
        elif self._is_pair():
            self.rank = 2
            self.name = "Пара"
        else:
            self.rank = 1
            self.name = "Старшая карта" 