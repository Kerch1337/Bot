from aiogram import Router, types, F
from aiogram.types import FSInputFile
from pathlib import Path
from utils.logger import logger
from aiogram.types import Message
from datetime import datetime
from database.model import Message as MessageModel
from .commands import get_or_create_user
from sqlalchemy.orm import Session

router = Router()

@router.message(F.text)
async def handle_and_save_message(message: Message, session: Session):
    try:
        tg_user = message.from_user
        user = get_or_create_user(session, tg_user)

        new_msg = MessageModel(
            text=message.text,
            sender_id=user.id,
            sent_at=datetime.utcnow()
        )
        session.add(new_msg)
        session.commit()

        logger.info(f"Сохранено сообщение от {tg_user.full_name} (id={user.id})")
    except Exception as e:
        logger.error(f"Ошибка сохранения сообщения: {str(e)}")
        session.rollback()

    # Ответ пользователю
    user_text = message.text.lower()
    if user_text == "привет":
        await message.answer("И тебе привет! 😊")
    elif user_text == "помощь":
        await message.answer("Вот доступные команды:\n/start - начать заново\n/re_chat - история сообщений")
    elif user_text == "мои данные":
        await message.answer(
            f"Ваши данные:\n"
            f"ID: {tg_user.id}\n"
            f"Имя: {tg_user.first_name}\n"
            f"Фамилия: {tg_user.last_name or 'нет'}\n"
            f"Username: @{tg_user.username}"
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