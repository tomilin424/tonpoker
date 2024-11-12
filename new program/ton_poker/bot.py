from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import asyncio
import logging
from datetime import datetime
from typing import Dict, List
import random
from game_logic import PokerTable
from prize_system import PrizeSystem
from poker_combinations import Card, PokerHand
from statistics import PlayerStatistics
from tournament_system import TournamentSystem
from chat_system import ChatSystem
from achievements import AchievementSystem
from notifications import NotificationSystem

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашего бота
TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

# Глобальные хранилища
PLAYERS: Dict[int, Dict] = {}
TOURNAMENTS: Dict[str, Dict] = {
    'sng_6': {
        'name': '🔥 Sit & Go (6 max)',
        'buy_in': 5,
        'players': [],
        'max_players': 6,
        'prize_pool': 0,
        'status': 'registering',
        'starting_chips': 1500,
    },
    'sng_9': {
        'name': '🌟 Sit & Go (9 max)',
        'buy_in': 10,
        'players': [],
        'max_players': 9,
        'prize_pool': 0,
        'status': 'registering',
        'starting_chips': 2000,
    }
}
ACTIVE_GAMES: Dict[str, PokerTable] = {}
PRIZE_SYSTEM = PrizeSystem()

# Система рейтинга
class RatingSystem:
    def __init__(self):
        self.ratings = {}
    
    def update_rating(self, user_id: int, tournament_result: Dict):
        if user_id not in self.ratings:
            self.ratings[user_id] = {
                'rating': 1000,
                'tournaments_played': 0,
                'tournaments_won': 0,
                'total_winnings': 0
            }
        
        player = self.ratings[user_id]
        player['tournaments_played'] += 1
        
        if tournament_result['position'] == 1:
            player['tournaments_won'] += 1
            player['rating'] += 50
        else:
            player['rating'] += max(0, 10 - tournament_result['position']) * 5
        
        player['total_winnings'] += tournament_result['prize']

# Система достижений
ACHIEVEMENT_SYSTEM = AchievementSystem()

# Инициализация статистики
STATS = PlayerStatistics()

# Система турниров
TOURNAMENT_SYSTEM = TournamentSystem()

# Система чата
CHAT_SYSTEM = ChatSystem()

# Система уведомлений
NOTIFICATION_SYSTEM = None  # Будет инициализирован в main()

async def start_command(update: Update, context):
    """Обработчик команды /start"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 Играть", callback_data="play"),
            InlineKeyboardButton("💰 Баланс", callback_data="balance")
        ],
        [
            InlineKeyboardButton("🏆 Турниры", callback_data="tournaments"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Привет! Я покер-бот.\n"
        "🎮 Выбери действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()  # Отвечаем на callback query
    
    if query.data == "play":
        await query.edit_message_text(
            "🎮 Выберите тип игры:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Sit & Go (6 max)", callback_data="sng_6")],
                [InlineKeyboardButton("🌟 Sit & Go (9 max)", callback_data="sng_9")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
    elif query.data == "balance":
        await query.edit_message_text(
            "💰 Ваш баланс: 0 TON\n\n"
            "Для пополнения используйте команду /deposit",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )
    elif query.data == "tournaments":
        await query.edit_message_text(
            "🏆 Доступные турниры:\n\n"
            "Пока нет активных турниров",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
            ]])
        )
    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ Доступные команды:\n"
            "/start - Главное меню\n"
            "/help - Помощь\n"
            "/play - Начать игру\n"
            "/balance - Проверить баланс",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(" Назад", callback_data="back_to_menu")
            ]])
        )
    elif query.data == "back_to_menu":
        keyboard = [
            [
                InlineKeyboardButton("🎮 Играть", callback_data="play"),
                InlineKeyboardButton("💰 Баланс", callback_data="balance")
            ],
            [
                InlineKeyboardButton("🏆 Турниры", callback_data="tournaments"),
                InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
            ]
        ]
        await query.edit_message_text(
            "👋 Главное меню\n"
            "🎮 Выбери действие:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def show_tournament_info(query, tournament_id):
    """Показывает информацию о турнире"""
    tournament = TOURNAMENTS[tournament_id]
    
    message = (
        f"🏆 {tournament['name']}\n\n"
        f"💰 Buy-in: {tournament['buy_in']} TON\n"
        f"👥 Игроков: {len(tournament['players'])}/{tournament['max_players']}\n"
        f"🎯 Призовой фонд: {tournament['prize_pool']} TON\n"
        f"💎 Стартовый стек: {tournament['starting_chips']}\n\n"
        "Зарегистрированные игроки:\n"
    )
    
    for player in tournament['players']:
        message += f"• {player['username']}\n"
    
    keyboard = [
        [InlineKeyboardButton("✅ Регистрация", callback_data=f"register_{tournament_id}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="tournaments")]
    ]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def register_tournament(query, tournament_id):
    """Регистрация в турнир"""
    user_id = query.from_user.id
    username = query.from_user.username or f"Player_{user_id}"
    tournament = TOURNAMENTS[tournament_id]
    
    # Проверяем, не зарегистрирован ли уже игрок
    if any(p['user_id'] == user_id for p in tournament['players']):
        await query.answer("Вы уже зарегистрированы в этот турнир!", show_alert=True)
        return
    
    # Проверяем количество игроков
    if len(tournament['players']) >= tournament['max_players']:
        await query.answer("Турнир уже заполнен!", show_alert=True)
        return
    
    # Проверяем баланс (здесь нужно будет дбавить реальную проверку)
    player_balance = PLAYERS.get(user_id, {}).get('balance', 0)
    if player_balance < tournament['buy_in']:
        await query.answer(
            f"Недостаточно средс��в! Необходимо: {tournament['buy_in']} TON",
            show_alert=True
        )
        return
    
    # Регистрируем игрока
    tournament['players'].append({
        'user_id': user_id,
        'username': username,
        'registered_at': datetime.now()
    })
    tournament['prize_pool'] += tournament['buy_in']
    
    # Если турнир заполнен, начинаем его
    if len(tournament['players']) >= tournament['max_players']:
        tournament['status'] = 'starting'
        # Здесь будет логика начала турнира
    
    await show_tournament_info(query, tournament_id)

async def update_tournament_status(tournament_id: str, context):
    """Обновляет статус турнира и начинает игру при необходимости"""
    tournament = TOURNAMENTS[tournament_id]
    if len(tournament['players']) >= tournament['max_players']:
        tournament['status'] = 'starting'
        prizes = PRIZE_SYSTEM.calculate_prizes(tournament['buy_in'], len(tournament['players']))
        tournament['prizes'] = prizes
        await start_tournament_game(tournament_id, context)

async def start_tournament_game(tournament_id: str, context):
    """Наинает игру в турнире"""
    tournament = TOURNAMENTS[tournament_id]
    table = PokerTable(tournament_id, tournament['players'])
    ACTIVE_GAMES[tournament_id] = table
    
    # Раздаем карты и начинаем игру
    table.deal_cards()
    
    # Уведомляем всех игроков
    for player in tournament['players']:
        user_id = player['user_id']
        player_cards = table.players[user_id]['cards']
        
        message = (
            "🎮 Игра началась!\n\n"
            f"Ваши карты: {' '.join(str(card) for card in player_cards)}\n"
            f"Фишки: {table.players[user_id]['chips']}"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Чек", callback_data=f"game_check_{tournament_id}"),
                InlineKeyboardButton("📈 Рейз", callback_data=f"game_raise_{tournament_id}"),
                InlineKeyboardButton("❌ Фолд", callback_data=f"game_fold_{tournament_id}")
            ]
        ]
        
        try:
            await context.bot.send_message(
                user_id,
                message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

async def handle_game_action(query: CallbackQuery, action: str, tournament_id: str):
    """Обработчик игровых действий"""
    user_id = query.from_user.id
    table = ACTIVE_GAMES.get(tournament_id)
    
    if not table or user_id not in table.players:
        await query.answer("Игра не найдена", show_alert=True)
        return
    
    player = table.players[user_id]
    
    if action == "check":
        if table.current_bet > 0:
            await query.answer("Нельзя сделать чек!", show_alert=True)
            return
            
        # Обновляем статистику
        STATS.update_stats(user_id, 'hand_played', {
            'action': 'check',
            'hand_rank': table.evaluate_hand(user_id)['rank']
        })
        
        # Переход к следующему игроку
        await next_player_turn(table, tournament_id, context)
    
    elif action == "raise":
        possible_bets = []
        min_raise = max(table.big_blind, table.current_bet * 2)
        
        for multiplier in [1, 1.5, 2, 3]:
            bet = int(min_raise * multiplier)
            if bet <= player['chips']:
                possible_bets.append(bet)
        
        keyboard = []
        for bet in possible_bets:
            keyboard.append([InlineKeyboardButton(
                f"Поставить {bet}", 
                callback_data=f"game_bet_{tournament_id}_{bet}"
            )])
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=f"game_back_{tournament_id}")])
        
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif action == "fold":
        player['status'] = 'folded'
        STATS.update_stats(user_id, 'hand_played', {'action': 'fold'})
        
        # Проверяем, остался ли один игрок
        active_players = [p for p in table.players.values() if p['status'] == 'active']
        if len(active_players) == 1:
            await end_hand(table, tournament_id, context)
        else:
            await next_player_turn(table, tournament_id, context)

async def end_hand(table: PokerTable, tournament_id: str, context):
    """Завершает раздачу"""
    result = table.determine_winner()
    winner_id = result['winner_id']
    
    # Обновляем статистику
    STATS.update_stats(winner_id, 'hand_played', {
        'won': True,
        'pot': result['pot'],
        'hand_rank': result['hand']['rank'] if result['hand'] else 0,
        'hand_name': result['hand']['name'] if result['hand'] else 'Default win'
    })
    
    # Уведомляем игроков
    for user_id in table.players:
        message = (
            f"🏆 Победитель: {table.players[winner_id]['username']}\n"
            f"💰 Банк: {result['pot']} фишек\n"
        )
        if result['hand']:
            message += f"🃏 Комбинация: {result['hand']['name']}"
        
        try:
            await context.bot.send_message(user_id, message)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
    
    # Начинаем новую раздачу
    await start_new_hand(table, tournament_id, context)

async def show_player_stats(query: CallbackQuery, user_id: int):
    """Показывает статистику игрока"""
    stats = STATS.get_player_stats(user_id)
    rating = RATING_SYSTEM.ratings.get(user_id, {'rating': 1000})
    achievements = ACHIEVEMENT_SYSTEM.player_achievements.get(user_id, [])
    
    message = (
        "📊 Ваша статистика:\n\n"
        f"🏆 Рейтинг: {rating['rating']}\n"
        f"🎮 Турниров сыграно: {stats.get('tournaments_played', 0)}\n"
        f"👑 Турниров выиграно: {stats.get('tournaments_won', 0)}\n"
        f"💰 Общий выигрыш: {stats.get('total_winnings', 0)} TON\n"
        f"🎯 Сыграно раздач: {stats.get('hands_played', 0)}\n"
        f"✨ Выиграно раздач: {stats.get('hands_won', 0)}\n\n"
    )
    
    if stats.get('best_hand'):
        message += (
            "🃏 Лучшая комбинация:\n"
            f"{stats['best_hand']['name']}\n"
            f"Получена: {stats['best_hand']['date']}\n\n"
        )
    
    if achievements:
        message += "🏅 Достижения:\n"
        for achievement in achievements:
            ach_data = ACHIEVEMENT_SYSTEM.achievements[achievement]
            message += f"• {ach_data['name']} - {ach_data['description']}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_bet(query: CallbackQuery, tournament_id: str, bet_amount: int):
    """Обрабатывает ставку игрока"""
    user_id = query.from_user.id
    table = ACTIVE_GAMES.get(tournament_id)
    
    if not table or user_id not in table.players:
        await query.answer("Игра не найдена", show_alert=True)
        return
    
    player = table.players[user_id]
    result = table.place_bet(user_id, bet_amount)
    
    if result['status'] == 'success':
        # Обновляем статистику
        STATS.update_stats(user_id, 'hand_played', {
            'action': 'bet',
            'amount': bet_amount
        })
        
        # Уведомляем всех игроков о ставке
        for pid in table.players:
            try:
                await context.bot.send_message(
                    pid,
                    f"💰 {player['username']} ставит {bet_amount} фишек"
                )
            except Exception as e:
                print(f"Error sending message to {pid}: {e}")
        
        # Если игрок пошел олл-ин
        if result['is_all_in']:
            await handle_all_in(table, tournament_id, user_id, context)
        else:
            await next_player_turn(table, tournament_id, context)
    else:
        await query.answer("Ошибка при размещении ставки", show_alert=True)

async def handle_all_in(table: PokerTable, tournament_id: str, user_id: int, context):
    """Обрабатывает ситуацию олл-ина"""
    # Проверяем, все ли игроки в олл-ине
    active_players = [p for p in table.players.values() if p['status'] == 'active']
    all_in_players = [p for p in table.players.values() if p['status'] == 'all-in']
    
    if len(active_players) == 0 or (len(active_players) == 1 and len(all_in_players) > 0):
        # Раскрываем все оставшиеся карты
        while len(table.community_cards) < 5:
            table.deal_community_cards(1)
        
        # Определяем победителя
        await end_hand(table, tournament_id, context)
    else:
        await next_player_turn(table, tournament_id, context)

async def handle_chat_message(update: Update, context):
    """Обрабатывает сообщения в чате турнира"""
    message = update.message
    user_id = message.from_user.id
    
    # Находим активный турнир игрока
    active_tournament = None
    for t_id, tournament in TOURNAMENT_SYSTEM.tournaments.items():
        if any(p['user_id'] == user_id for p in tournament['players']):
            active_tournament = tournament
            break
    
    if not active_tournament:
        return
    
    # Добавляем сообщение в чат
    CHAT_SYSTEM.add_message(
        active_tournament['id'],
        user_id,
        message.from_user.username,
        message.text
    )
    
    # Отправляем сообщение всем игрокам турнира
    for player in active_tournament['players']:
        if player['user_id'] != user_id:  # Не отправляем сообщение отправителю
            try:
                await context.bot.send_message(
                    player['user_id'],
                    f"💭 {message.from_user.username}: {message.text}"
                )
            except Exception as e:
                print(f"Error sending message to {player['user_id']}: {e}")

async def show_tournament_chat(query: CallbackQuery, tournament_id: str):
    """Показывает чат турнира"""
    messages = CHAT_SYSTEM.get_messages(tournament_id)
    
    message = "💭 Чат турнира:\n\n"
    for msg in messages:
        message += f"@{msg['username']}: {msg['text']}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data=f"tournament_{tournament_id}")]]
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_achievement(user_id: int, event: str, data: Dict):
    """Обрабатывает получение достижений"""
    earned_achievements = ACHIEVEMENT_SYSTEM.check_achievements(user_id, event, data)
    
    for achievement in earned_achievements:
        # Начисляем награду
        PLAYERS[user_id]['balance'] += achievement.reward
        
        # Отправляем уведомление
        await NOTIFICATION_SYSTEM.notify_achievement(user_id, achievement)

def main():
    global NOTIFICATION_SYSTEM
    
    app = Application.builder().token(TOKEN).build()
    NOTIFICATION_SYSTEM = NotificationSystem(app.bot)
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat_message))
    
    print("Бот запущен!")
    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()
