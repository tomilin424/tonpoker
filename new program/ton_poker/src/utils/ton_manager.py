from tonsdk.utils import to_nano
import aiohttp
import json
from typing import Dict

class TonManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://toncenter.com/api/v2"
        self.headers = {"X-API-Key": api_key}
        
    async def create_wallet(self) -> Dict:
        """Создает новый кошелек"""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"{self.base_url}/create_wallet") as response:
                data = await response.json()
                return {
                    'address': data['address'],
                    'public_key': data['public_key'],
                    'private_key': data['private_key']
                }
    
    async def get_balance(self, address: str) -> float:
        """Получает баланс кошелька"""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(
                f"{self.base_url}/getAddressBalance",
                params={"address": address}
            ) as response:
                data = await response.json()
                return float(data['balance']) / 1e9
    
    async def send_transaction(self, from_wallet: Dict, to_address: str, amount: float) -> Dict:
        """Отправляет TON"""
        params = {
            "from": from_wallet['address'],
            "to": to_address,
            "amount": to_nano(amount),
            "private_key": from_wallet['private_key']
        }
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                f"{self.base_url}/sendTransaction",
                json=params
            ) as response:
                return await response.json() 