from aiogram import Dispatcher
from utils.logger import logger
from database.db import Base, init_db, get_db_session
from handlers import commands, messages
from dotenv import load_dotenv
import os

# Инициализация бота должна происходить ПОСЛЕ инициализации БД
# Чтобы избежать циклических импортов, выносим инициализацию бота в этот файл
from aiogram import Bot

load_dotenv('.env', encoding='utf-8')
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def register_handlers(dp: Dispatcher):
    dp.include_routers(commands.router, messages.router)

def on_startup():
    """Действия при запуске бота"""
    try:
        engine, _ = init_db()
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы БД успешно верифицированы")
    except Exception as e:
        logger.critical(f"Ошибка инициализации БД: {str(e)}")
        # Выход при критической ошибке БД
        exit(1)

if __name__ == "__main__":
    # Регистрация обработчиков
    register_handlers(dp)
    dp.startup.register(on_startup)
    
    logger.info("Бот запущен и ожидает сообщений...")
    dp.run_polling(bot)