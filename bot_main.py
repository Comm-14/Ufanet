import asyncio
import logging
from aiogram import Bot, Dispatcher

from bot_test.handlers import router
from config import TOKEN


# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# Объект бота


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Бот запущен")
    except KeyboardInterrupt:
        print("Бот выключен")