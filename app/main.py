from bot import dp, bot
from utils.logger import logger
from aiogram import Dispatcher

from handlers import commands, messages


def register_handlers(dp: Dispatcher):
    dp.include_routers(commands.router, messages.router)


if __name__ == "__main__":
    register_handlers(dp)
    logger.info("Бот запущен и ожидает сообщений...")
    dp.run_polling(bot)