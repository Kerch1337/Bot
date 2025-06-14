import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from utils.logger import logger
from database.db import init_db, get_session
from handlers import commands, messages
from dotenv import load_dotenv
import os
from middlewares.middleware import DbSessionMiddleware

load_dotenv('.env', encoding='utf-8')
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

def register_handlers(dp: Dispatcher):
    dp.include_routers(commands.router, messages.router)

async def main():
    await init_db()  # корректный async вызов
    logger.info("Таблицы БД успешно верифицированы")

    session_factory = get_session()
    dp.update.middleware(DbSessionMiddleware(session_factory))
    register_handlers(dp)

    logger.info("Бот запущен и ожидает сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
