from typing import List, Dict
from decimal import Decimal

class PrizeSystem:
    def __init__(self):
        self.prize_structures = {
            6: [0.5, 0.3, 0.2],  # 50%, 30%, 20%
            9: [0.4, 0.25, 0.2, 0.15]  # 40%, 25%, 20%, 15%
        }
    
    def calculate_prizes(self, buy_in: float, players_count: int) -> List[Dict]:
        """Рассчитывает призовые места"""
        total_prize = Decimal(str(buy_in)) * players_count
        structure = self.prize_structures[min(k for k in self.prize_structures.keys() 
                                           if k >= players_count)]
        
        prizes = []
        for i, percentage in enumerate(structure):
            prize_amount = float(total_prize * Decimal(str(percentage)))
            prizes.append({
                'place': i + 1,
                'amount': prize_amount,
                'percentage': percentage * 100
            })
        
        return prizes 