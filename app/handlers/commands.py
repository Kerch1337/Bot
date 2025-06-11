from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import get_main_keyboard
from utils.logger import logger

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    logger.info(f"Пользователь {message.from_user.full_name} начал общение")
    user = message.from_user
    await message.answer(
        f"Привет, {user.first_name}! Я просто бот. Можешь написать что-нибудь или выбрать команду:",
        reply_markup=get_main_keyboard()
    )