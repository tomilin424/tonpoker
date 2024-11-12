import aiosqlite
import asyncio
from typing import Dict, List
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = 'poker.db'):
        self.db_path = db_path
        
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    balance REAL DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    tournaments_won INTEGER DEFAULT 0,
                    rating INTEGER DEFAULT 1000,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    type TEXT,
                    amount REAL,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES players (user_id)
                )
            ''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS tournaments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tournament_type TEXT,
                    buy_in REAL,
                    status TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    prize_pool REAL DEFAULT 0
                )
            ''')
            
            await db.commit()
    
    async def get_player(self, user_id: int) -> Dict:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT * FROM players WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
    
    async def create_player(self, user_id: int, username: str) -> Dict:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT INTO players (user_id, username) VALUES (?, ?)',
                (user_id, username)
            )
            await db.commit()
            return await self.get_player(user_id) 