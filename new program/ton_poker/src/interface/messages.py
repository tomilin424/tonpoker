class Messages:
    WELCOME = """
👋 Добро пожаловать в TON Poker!

🎮 Играйте в покер на TON
💰 Выигрывайте призы
🏆 Участвуйте в турнирах

Выберите действие:
"""

    HELP = """
ℹ️ Помощь по игре:

🎮 Как играть:
1. Пополните баланс
2. Выберите турнир
3. Играйте и выигрывайте!

💰 Депозит и вывод:
• Минимальный депозит: 5 TON
• Минимальный вывод: 10 TON

🏆 Турниры:
• Sit & Go (6 max) - бай-ин 5 TON
• Sit & Go (9 max) - бай-ин 10 TON

📞 Поддержка: @support_bot
"""

    BALANCE = """
💰 Ваш баланс: {balance} TON

🎮 Игр сыграно: {games_played}
🏆 Турниров выиграно: {tournaments_won}
📈 Рейтинг: {rating}
"""

    TOURNAMENT_INFO = """
🏆 {name}

💰 Бай-ин: {buy_in} TON
👥 Игроков: {players}/{max_players}
🎯 Призовой фонд: {prize_pool} TON
💎 Стартовый стек: {starting_chips}

Статус: {status}
""" 