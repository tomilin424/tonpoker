from typing import Dict, List
from decimal import Decimal

class PrizeManager:
    def __init__(self, db_manager, ton_manager):
        self.db = db_manager
        self.ton = ton_manager
        
        self.prize_structures = {
            6: [0.5, 0.3, 0.2],  # 50%, 30%, 20%
            9: [0.4, 0.25, 0.2, 0.15]  # 40%, 25%, 20%, 15%
        }
    
    async def calculate_prizes(self, tournament_id: str) -> List[Dict]:
        """Рассчитывает призовые места"""
        async with self.db.pool.acquire() as conn:
            tournament = await conn.fetchrow(
                'SELECT * FROM tournaments WHERE id = ?',
                tournament_id
            )
            
            players = await conn.fetch(
                'SELECT * FROM tournament_players WHERE tournament_id = ?',
                tournament_id
            )
            
            prize_pool = Decimal(str(tournament['prize_pool']))
            structure = self.prize_structures[min(k for k in self.prize_structures.keys() 
                                               if k >= len(players))]
            
            prizes = []
            for i, percentage in enumerate(structure):
                prize_amount = float(prize_pool * Decimal(str(percentage)))
                prizes.append({
                    'place': i + 1,
                    'amount': prize_amount,
                    'percentage': percentage * 100
                })
            
            return prizes
    
    async def distribute_prizes(self, tournament_id: str, final_positions: List[Dict]):
        """Распределяет призы после турнира"""
        prizes = await self.calculate_prizes(tournament_id)
        
        for position in final_positions:
            for prize in prizes:
                if position['position'] == prize['place']:
                    user_id = position['user_id']
                    amount = prize['amount']
                    
                    # Начисляем приз игроку
                    async with self.db.pool.acquire() as conn:
                        await conn.execute(
                            'UPDATE players SET balance = balance + ? WHERE user_id = ?',
                            (amount, user_id)
                        )
                        
                        # Записываем транзакцию
                        await conn.execute(
                            '''INSERT INTO transactions 
                               (user_id, type, amount, status, tournament_id) 
                               VALUES (?, ?, ?, ?, ?)''',
                            (user_id, 'prize', amount, 'completed', tournament_id)
                        )
                    
                    # Отправляем уведомление
                    try:
                        await self.bot.send_message(
                            user_id,
                            f"🏆 Поздравляем!\n\n"
                            f"Вы заняли {prize['place']} место\n"
                            f"Выигрыш: {amount} TON"
                        )
                    except Exception as e:
                        print(f"Error sending prize notification to {user_id}: {e}") 