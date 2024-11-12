from typing import Dict, List
from datetime import datetime
import asyncio

class NotificationSystem:
    def __init__(self, bot):
        self.bot = bot
        self.notifications = {}  # user_id -> [notifications]
    
    async def send_notification(self, user_id: int, message: str, markup=None):
        """Отправляет уведомление пользователю"""
        try:
            await self.bot.send_message(
                user_id,
                message,
                reply_markup=markup
            )
            
            if user_id not in self.notifications:
                self.notifications[user_id] = []
            
            self.notifications[user_id].append({
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error sending notification to {user_id}: {e}")
    
    async def notify_achievement(self, user_id: int, achievement: Achievement):
        """Уведомляет о получении достижения"""
        message = (
            f"🎉 Новое достижение!\n\n"
            f"{achievement.icon} {achievement.name}\n"
            f"📝 {achievement.description}\n"
            f"💰 Награда: {achievement.reward} TON"
        )
        await self.send_notification(user_id, message)
    
    async def notify_tournament_start(self, tournament_id: str, players: List[Dict]):
        """Уведомляет о начале турнира"""
        message = (
            "🎮 Турнир начинается!\n\n"
            "Удачной игры! Ваши карты будут отправлены отдельным сообщением."
        )
        
        for player in players:
            await self.send_notification(player['user_id'], message)
    
    async def notify_hand_result(self, user_id: int, result: Dict):
        """Уведомляет о результатах раздачи"""
        if result['won']:
            message = (
                "🏆 Вы выиграли раздачу!\n\n"
                f"💰 Банк: {result['pot']} фишек\n"
                f"🃏 Комбинация: {result['hand_name']}"
            )
        else:
            message = "❌ Вы проиграли раздачу"
        
        await self.send_notification(user_id, message) 