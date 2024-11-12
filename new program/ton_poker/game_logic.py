from typing import List, Dict
import random
from poker_combinations import Card, PokerHand
from betting import BettingManager

class PokerTable:
    def __init__(self, tournament_id: str, players: List[Dict]):
        self.tournament_id = tournament_id
        self.players = {p['user_id']: {
            'username': p['username'],
            'chips': p['chips'],
            'cards': [],
            'bet': 0,
            'status': 'active',
            'position': i
        } for i, p in enumerate(players)}
        
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.current_player_idx = 0
        self.dealer_idx = 0
        self.betting_manager = BettingManager()
        self.round = 'preflop'  # preflop, flop, turn, river
        
    def post_blinds(self) -> List[Dict]:
        """Постит малый и большой блайнды"""
        blinds = self.betting_manager.get_current_blinds()
        actions = []
        
        # Находим игроков для блайндов
        positions = sorted(
            [(p['position'], user_id) for user_id, p in self.players.items()
             if p['status'] == 'active']
        )
        
        if len(positions) < 2:
            return actions
            
        # Малый блайнд
        sb_pos = (self.dealer_idx + 1) % len(positions)
        sb_player_id = positions[sb_pos][1]
        self.place_bet(sb_player_id, blinds.small_blind)
        actions.append({
            'player_id': sb_player_id,
            'action': 'small_blind',
            'amount': blinds.small_blind
        })
        
        # Большой блайнд
        bb_pos = (self.dealer_idx + 2) % len(positions)
        bb_player_id = positions[bb_pos][1]
        self.place_bet(bb_player_id, blinds.big_blind)
        actions.append({
            'player_id': bb_player_id,
            'action': 'big_blind',
            'amount': blinds.big_blind
        })
        
        # Анте
        if blinds.ante > 0:
            for user_id, player in self.players.items():
                if player['status'] == 'active':
                    self.place_bet(user_id, blinds.ante)
                    actions.append({
                        'player_id': user_id,
                        'action': 'ante',
                        'amount': blinds.ante
                    })
        
        return actions
    
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