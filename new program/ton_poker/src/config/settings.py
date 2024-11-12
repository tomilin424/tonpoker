import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

# TON settings
TON_API_KEY = "YOUR_TON_API_KEY"  # Получите ключ на https://toncenter.com
TON_ENDPOINT = "https://toncenter.com/api/v2"

# Game settings
TOURNAMENT_TYPES = {
    'sng_6': {
        'name': '🔥 Sit & Go (6 max)',
        'buy_in': 5,
        'max_players': 6,
        'starting_chips': 1500,
        'blind_levels': [
            {'small': 10, 'big': 20, 'ante': 0, 'duration': 300},
            {'small': 15, 'big': 30, 'ante': 5, 'duration': 300},
            {'small': 25, 'big': 50, 'ante': 5, 'duration': 300},
        ]
    },
    'sng_9': {
        'name': '🌟 Sit & Go (9 max)',
        'buy_in': 10,
        'max_players': 9,
        'starting_chips': 2000,
        'blind_levels': [
            {'small': 10, 'big': 20, 'ante': 0, 'duration': 300},
            {'small': 20, 'big': 40, 'ante': 5, 'duration': 300},
        ]
    }
}

# Database settings
DATABASE_PATH = 'poker.db'

# Game constants
MIN_PLAYERS = 2
MAX_PLAYERS = 9
DEFAULT_CHIPS = 1500
MIN_BUY_IN = 5
MAX_BUY_IN = 1000

# Achievement rewards
ACHIEVEMENT_REWARDS = {
    'first_game': 1,
    'first_win': 5,
    'high_roller': 10,
    'winning_streak': 20,
    'royal_flush': 50
} 