from typing import Dict, List
import random

class Card:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        suits = {'♠': '♠', '♣': '♣', '♥': '♥', '♦': '♦'}
        values = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        return f"{values.get(self.value, str(self.value))}{suits[self.suit]}"

class PokerGame:
    def __init__(self, game_id: str, players: List[Dict]):
        self.game_id = game_id
        self.players = {p['user_id']: {
            'username': p['username'],
            'chips': p['chips'],
            'cards': [],
            'bet': 0,
            'status': 'active'
        } for p in players}
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.current_player_idx = 0
        
    def init_deck(self):
        """Инициализация колоды"""
        suits = ['♠', '♣', '♥', '♦']
        values = range(2, 15)
        self.deck = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.deck)
    
    def deal_cards(self):
        """Раздача карт игрокам"""
        self.init_deck()
        for _ in range(2):
            for player in self.players.values():
                if player['status'] == 'active':
                    player['cards'].append(self.deck.pop())
    
    def deal_community_cards(self, count: int = 1):
        """Раздача общих карт"""
        for _ in range(count):
            if len(self.deck) > 0:
                self.community_cards.append(self.deck.pop())
    
    def place_bet(self, user_id: int, amount: int) -> Dict:
        """Размещает ставку игрока"""
        player = self.players[user_id]
        
        if amount > player['chips']:
            amount = player['chips']
            player['status'] = 'all-in'
            
        player['chips'] -= amount
        player['bet'] += amount
        self.pot += amount
        self.current_bet = max(self.current_bet, player['bet'])
        
        return {
            'status': 'success',
            'amount': amount,
            'remaining_chips': player['chips'],
            'is_all_in': player['status'] == 'all-in'
        } 