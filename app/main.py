# main.py
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from utils.logger import logger
from database.db import Base, init_db, get_session
from handlers import commands, messages
from dotenv import load_dotenv
import os
from contextlib import contextmanager
from sqlalchemy.orm import Session
from middlewares.middleware import DbSessionMiddleware

load_dotenv('.env', encoding='utf-8')
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@contextmanager
def lifespan():
    engine, _ = init_db()
    Base.metadata.create_all(bind=engine)
    logger.info("Таблицы БД успешно верифицированы")
    yield

def register_handlers(dp: Dispatcher):
    dp.include_routers(commands.router, messages.router)

if __name__ == "__main__":
    session_factory = get_session()
    dp.update.middleware(DbSessionMiddleware(session_factory))
    register_handlers(dp)
    
    logger.info("Бот запущен и ожидает сообщений...")
    dp.run_polling(bot)