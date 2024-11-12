from telegram.ext import Application, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Токен вашего бота
TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

# Обработчик команды /start
async def start(update, context):
    text = "Привет! Я покер-бот!"
    await update.message.reply_text(text)

# Основная функция
async def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    print("Bot started!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main()) 