from typing import Dict, List
import math

class RatingManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.k_factor = 32  # Фактор изменения рейтинга
    
    async def update_ratings(self, tournament_id: str, final_positions: List[Dict]):
        """Обновляет рейтинги игроков после турнира"""
        players = []
        async with self.db.pool.acquire() as conn:
            for position in final_positions:
                player = await conn.fetchrow(
                    'SELECT * FROM players WHERE user_id = ?',
                    position['user_id']
                )
                players.append({
                    'user_id': player['user_id'],
                    'rating': player['rating'],
                    'position': position['position']
                })
        
        # Обновляем рейтинги
        for i, player1 in enumerate(players):
            rating_change = 0
            for j, player2 in enumerate(players):
                if i != j:
                    # Вычисляем ожидаемый результат
                    expected = 1 / (1 + math.pow(
                        10, 
                        (player2['rating'] - player1['rating']) / 400
                    ))
                    
                    # Вычисляем фактический результат
                    actual = 1 if player1['position'] < player2['position'] else 0
                    
                    # Обновляем изменение рейтинга
                    rating_change += self.k_factor * (actual - expected)
            
            # Применяем изменение рейтинга
            new_rating = max(1, int(player1['rating'] + rating_change))
            
            async with self.db.pool.acquire() as conn:
                await conn.execute(
                    'UPDATE players SET rating = ? WHERE user_id = ?',
                    (new_rating, player1['user_id'])
                ) 