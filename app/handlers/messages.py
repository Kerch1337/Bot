from aiogram import Router, types
from aiogram.types import FSInputFile
from pathlib import Path
from utils.logger import logger

router = Router()

@router.message()
async def handle_message(message: types.Message):
    user_text = message.text.lower()
    logger.info(f"Пользователь написал: {user_text}")

    if user_text == "привет":
        await message.answer("И тебе привет! 😊")
    elif user_text == "помощь":
        await message.answer("Вот доступные команды:\n/start - начать заново")
    elif user_text == "мои данные":
        user = message.from_user
        await message.answer(
            f"Ваши данные:\n"
            f"ID: {user.id}\n"
            f"Имя: {user.first_name}\n"
            f"Фамилия: {user.last_name or 'нет'}\n"
            f"Username: @{user.username}"
        )
    elif user_text == "окак":
        try:
            image_path = Path(__file__).parent.parent / "images" / "okak.jpg"
            if not image_path.exists():
                raise FileNotFoundError(f"Файл {image_path} не найден")

            photo = FSInputFile(image_path)
            await message.answer_photo(photo, caption="окак")
        except Exception as e:
            logger.error(f"Ошибка отправки изображения: {e}")
            await message.answer("Не удалось загрузить изображение 😢")
    else:
        await message.answer(user_text[::-1])
