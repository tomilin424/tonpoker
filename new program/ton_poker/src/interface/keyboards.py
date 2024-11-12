from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
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
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def tournament_menu() -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton("🔥 Sit & Go (6 max)", callback_data="sng_6")],
            [InlineKeyboardButton("🌟 Sit & Go (9 max)", callback_data="sng_9")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def balance_menu() -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton("📥 Депозит", callback_data="deposit"),
                InlineKeyboardButton("📤 Вывод", callback_data="withdraw")
            ],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        return InlineKeyboardMarkup(keyboard) 