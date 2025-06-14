from aiogram import Router, F
from aiogram.types import FSInputFile, Message
from pathlib import Path
from utils.logger import logger
from datetime import datetime
from database.model import Message as MessageModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.openai_client import chat_with_gpt
from .commands import get_or_create_user
from services.openai_client import get_or_create_dialogue

router = Router()

@router.message(F.text)
async def handle_and_save_message(message: Message, session: AsyncSession):
    tg_user = message.from_user
    user = await get_or_create_user(session, tg_user)
    user_text = message.text.strip().lower()

    # Сохраняем сообщение пользователя
    try:
        dialogue = await get_or_create_dialogue(session, user)

        new_msg = MessageModel(
            text=message.text,
            sender_id=user.id,
            dialogue=dialogue,
            sent_at=datetime.utcnow()
        )
        session.add(new_msg)
        await session.commit()
        logger.info(f"Сохранено сообщение от {tg_user.full_name} (id={user.id})")
    except Exception as e:
        logger.error(f"Ошибка сохранения сообщения: {str(e)}")
        await session.rollback()

    # Ответы на команды
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
        # GPT-ответ
        try:
            reply = await chat_with_gpt(session, user, message.text)
            await message.answer(reply)
            logger.info(f"Ответ от GPT отправлен пользователю {tg_user.full_name}")
        except Exception as e:
            logger.error(f"Ошибка при обращении к GPT: {str(e)}")
            await message.answer("⚠️ Произошла ошибка при обработке запроса.")
