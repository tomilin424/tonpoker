from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

# Для тестирования используем тестовый сервер Telegram
WEB_APP_URL = "https://test-telegram-web-app.herokuapp.com"

class TonPokerBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.register_handlers()
    
    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
    
    async def start_command(self, update: Update, context):
        # Устанавливаем кнопку меню
        await context.bot.set_chat_menu_button(
            chat_id=update.effective_chat.id,
            menu_button=MenuButtonWebApp(text="🎮 Играть в покер", web_app=WebAppInfo(url=WEB_APP_URL))
        )
        
        keyboard = [
            [
                InlineKeyboardButton("💰 Баланс", callback_data="balance"),
                InlineKeyboardButton("🏆 Турниры", callback_data="tournaments")
            ],
            [
                InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 Добро пожаловать в TON Poker!\n"
            "🎮 Нажмите кнопку меню чтобы начать игру",
            reply_markup=reply_markup
        )
    
    async def button_handler(self, update: Update, context):
        query = update.callback_query
        await query.answer()
        
        if query.data == "balance":
            await query.edit_message_text(
                "💰 Ваш баланс: 0 TON",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
        elif query.data == "tournaments":
            await query.edit_message_text(
                "🏆 Доступные турниры:\n\n"
                "• Sit & Go (6 max) - 5 TON\n"
                "• Sit & Go (9 max) - 10 TON",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
            )
        elif query.data == "help":
            await query.edit_message_text(
                "ℹ️ Как играть:\n\n"
                "1. Нажмите кнопку меню '🎮 Играть в покер'\n"
                "2. Выберите тип игры\n"
                "3. Наслаждайтесь игрой!\n\n"
                "💰 Минимальный депозит: 5 TON\n"
                "🏆 Доступны турниры Sit & Go",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")
                ]])
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