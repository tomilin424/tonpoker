from telegram.ext import Application, CommandHandler
import asyncio
import logging

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Ваш токен
TOKEN = "7334592326:AAHO5o_sw6sPoqKkdK_WMJumj1dtyaIcv0A"

async def start(update, context):
    logger.info("Получена команда /start")
    await update.message.reply_text("Привет! Бот запущен и работает!")

async def main():
    try:
        # Создаем приложение
        logger.info("Запуск бота...")
        app = Application.builder().token(TOKEN).build()

        # Добавляем обработчик команды /start
        app.add_handler(CommandHandler("start", start))

        # Запускаем бота
        logger.info("Бот успешно запущен!")
        await app.run_polling(allowed_updates=["message", "callback_query"])

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 