import logging
from telegram.ext import Application, CommandHandler

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашего бота
TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

# Обработчик команды /start
async def start(update, context):
    print("Получена команда /start")  # Отладочное сообщение
    await update.message.reply_text("Привет! Бот работает!")

async def main():
    try:
        # Создаем приложение
        print("Инициализация бота...")
        app = Application.builder().token(TOKEN).build()

        # Добавляем обработчик
        app.add_handler(CommandHandler("start", start))

        # Запускаем бота
        print("Бот запущен!")
        await app.run_polling()
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 