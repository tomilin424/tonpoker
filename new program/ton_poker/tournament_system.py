from typing import Dict, List
from datetime import datetime
from decimal import Decimal

class TournamentSystem:
    def __init__(self):
        self.tournaments = {}
        self.prize_structures = {
            6: [0.5, 0.3, 0.2],  # 50%, 30%, 20%
            9: [0.4, 0.25, 0.2, 0.15]  # 40%, 25%, 20%, 15%
        }
    
    def create_tournament(self, tournament_type: str, buy_in: float, max_players: int) -> str:
        """Создает новый турнир"""
        tournament_id = f"{tournament_type}_{int(datetime.now().timestamp())}"
        
        self.tournaments[tournament_id] = {
            'type': tournament_type,
            'buy_in': buy_in,
            'max_players': max_players,
            'players': [],
            'status': 'registering',
            'prize_pool': 0,
            'start_time': None,
            'end_time': None,
            'results': []
        }
        
        return tournament_id
    
    def register_player(self, tournament_id: str, user_id: int, username: str) -> Dict:
        """Регистрирует игрока в турнир"""
        tournament = self.tournaments.get(tournament_id)
        if not tournament:
            return {'status': 'error', 'message': 'Турнир не найден'}
            
        if len(tournament['players']) >= tournament['max_players']:
            return {'status': 'error', 'message': 'Турнир уже заполнен'}
            
        if any(p['user_id'] == user_id for p in tournament['players']):
            return {'status': 'error', 'message': 'Вы уже зарегистрированы'}
            
        tournament['players'].append({
            'user_id': user_id,
            'username': username,
            'status': 'active',
            'chips': tournament['buy_in'] * 100,  # Стартовый стек
            'position': None
        })
        
        tournament['prize_pool'] += tournament['buy_in']
        
        # Если турнир заполнен, меняем статус
        if len(tournament['players']) >= tournament['max_players']:
            tournament['status'] = 'starting'
            tournament['start_time'] = datetime.now()
        
        return {'status': 'success', 'tournament': tournament}
    
    def calculate_prizes(self, tournament_id: str) -> List[Dict]:
        """Рассчитывает призовые места"""
        tournament = self.tournaments[tournament_id]
        total_prize = Decimal(str(tournament['prize_pool']))
        player_count = len(tournament['players'])
        
        structure = self.prize_structures[min(k for k in self.prize_structures.keys() 
                                           if k >= player_count)]
        
        prizes = []
        for i, percentage in enumerate(structure):
            prize_amount = float(total_prize * Decimal(str(percentage)))
            prizes.append({
                'place': i + 1,
                'amount': prize_amount,
                'percentage': percentage * 100
            })
        
        return prizes
    
    def end_tournament(self, tournament_id: str, final_positions: List[Dict]) -> Dict:
        """Завершает турнир и распределяет призы"""
        tournament = self.tournaments[tournament_id]
        prizes = self.calculate_prizes(tournament_id)
        
        results = []
        for pos in final_positions:
            prize_amount = 0
            for prize in prizes:
                if prize['place'] == pos['position']:
                    prize_amount = prize['amount']
                    break
                    
            results.append({
                'user_id': pos['user_id'],
                'username': pos['username'],
                'position': pos['position'],
                'prize': prize_amount
            })
        
        tournament['status'] = 'completed'
        tournament['end_time'] = datetime.now()
        tournament['results'] = results
        
        return {'status': 'success', 'results': results} 