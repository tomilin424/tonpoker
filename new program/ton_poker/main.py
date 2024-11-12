from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"
WEB_APP_URL = "https://your-heroku-app.herokuapp.com"  # URL вашего приложения на Heroku

class TonPokerBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.register_handlers()
    
    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
    
    async def start_command(self, update: Update, context):
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
            "👋 Добро пожаловать в TON Poker!\n\n"
            "🎮 Выберите действие:",
            reply_markup=reply_markup
        )
    
    async def button_handler(self, update: Update, context):
        query = update.callback_query
        await query.answer()
        
        if query.data == "play":
            keyboard = [
                [InlineKeyboardButton("🔥 Sit & Go (6 max)", callback_data="sng_6")],
                [InlineKeyboardButton("🌟 Sit & Go (9 max)", callback_data="sng_9")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]
            await query.edit_message_text(
                "🎮 Выберите тип игры:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == "balance":
            keyboard = [
                [
                    InlineKeyboardButton("📥 Депозит", callback_data="deposit"),
                    InlineKeyboardButton("📤 Вывод", callback_data="withdraw")
                ],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]
            await query.edit_message_text(
                "💰 Ваш баланс: 0 TON",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == "tournaments":
            keyboard = [
                [InlineKeyboardButton("🔥 Регулярные турниры", callback_data="regular")],
                [InlineKeyboardButton("🌟 Специальные турниры", callback_data="special")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ]
            await query.edit_message_text(
                "🏆 Доступные турниры:\n\n"
                "• Sit & Go (6 max) - 5 TON\n"
                "• Sit & Go (9 max) - 10 TON\n"
                "• Daily Tournament - 25 TON",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == "help":
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
            await query.edit_message_text(
                "ℹ️ Как играть:\n\n"
                "1. Пополните баланс\n"
                "2. Выберите тип игры\n"
                "3. Присоединяйтесь к столу\n\n"
                "💰 Минимальный депозит: 5 TON\n"
                "📤 Минимальный вывод: 10 TON\n\n"
                "🏆 Доступные турниры:\n"
                "• Sit & Go (6 max)\n"
                "• Sit & Go (9 max)\n"
                "• Daily Tournament",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif query.data == "back_to_menu":
            await self.start_command(update, context)
    
    def run(self):
        print("Bot started! Press Ctrl+C to stop.")
        self.app.run_polling()

def main():
    bot = TonPokerBot()
    bot.run()

if __name__ == "__main__":
    main() 