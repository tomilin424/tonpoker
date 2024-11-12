from typing import Dict
from datetime import datetime
import asyncio
from .ton_manager import TonManager

class PaymentManager:
    def __init__(self, ton_manager: TonManager, db_manager):
        self.ton = ton_manager
        self.db = db_manager
        self.pending_deposits = {}
        
    async def create_deposit(self, user_id: int, amount: float) -> Dict:
        """Создает депозит"""
        wallet = await self.ton.create_wallet()
        
        self.pending_deposits[wallet['address']] = {
            'user_id': user_id,
            'amount': amount,
            'created_at': datetime.now(),
            'status': 'pending'
        }
        
        return {
            'address': wallet['address'],
            'amount': amount
        }
    
    async def check_deposits(self):
        """Проверяет статус депозитов"""
        while True:
            for address, deposit in self.pending_deposits.copy().items():
                try:
                    balance = await self.ton.get_balance(address)
                    if balance >= deposit['amount']:
                        # Подтверждаем депозит
                        await self.confirm_deposit(address, deposit)
                except Exception as e:
                    print(f"Error checking deposit {address}: {e}")
            
            await asyncio.sleep(10)  # Проверяем каждые 10 секунд
    
    async def confirm_deposit(self, address: str, deposit: Dict):
        """Подтверждает депозит"""
        user_id = deposit['user_id']
        amount = deposit['amount']
        
        # Обновляем баланс игрока
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                'UPDATE players SET balance = balance + ? WHERE user_id = ?',
                (amount, user_id)
            )
            
            # Записываем транзакцию
            await conn.execute(
                '''INSERT INTO transactions 
                   (user_id, type, amount, status) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, 'deposit', amount, 'completed')
            )
        
        # Удаляем из ожидающих
        del self.pending_deposits[address] 