# commands.py
from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database.model import User, Message, UserRole
from keyboards.reply import get_main_keyboard
from utils.logger import logger

router = Router()

def get_or_create_user(session, tg_user: types.User) -> User:
    try:
        user = session.scalar(
            select(User)
            .where(User.telegram_id == tg_user.id)
        )
        
        if not user:
            user = User(
                telegram_id=tg_user.id,
                first_name=tg_user.first_name,
                username=tg_user.username,
                last_name=tg_user.last_name,
                role=UserRole.USER  # Без .value
        )
            
            session.add(user)
            session.commit()
            logger.info(f"Создан новый пользователь: {user.id} ({tg_user.full_name})")
        return user
    except IntegrityError as e:
        session.rollback()
        user = session.scalar(
            select(User)
            .where(User.telegram_id == tg_user.id)
        )
        if user:
            logger.warning(f"Конфликт при создании пользователя, использован существующий: {user.id}")
            return user
        logger.error(f"Ошибка создания пользователя: {str(e)}")
        raise

@router.message(Command("start"))
async def start_command(message: types.Message, session: Session):
    try:
        tg_user = message.from_user
        user = get_or_create_user(session, tg_user)
        
        logger.info(f"Пользователь {tg_user.full_name} (id={user.id}) начал общение")
        await message.answer(
            f"Привет, {tg_user.first_name}! Я просто бот. Можешь написать что-нибудь или выбрать команду:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {str(e)}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")

@router.message(Command("re_chat"))
async def re_chat_command(message: types.Message, session: Session):
    try:
        args = message.text.split()[1:]
        target_id = None
        
        if args:
            try:
                target_id = int(args[0])
            except ValueError:
                await message.answer("❌ ID пользователя должен быть числом")
                return
        
        current_user = message.from_user
        if not target_id:
            target_id = current_user.id
        
        user = session.scalar(
            select(User)
            .where(User.telegram_id == target_id)
        )
        
        if not user:
            await message.answer(f"❌ Пользователь с ID {target_id} не найден")
            return
        
        messages = session.scalars(
            select(Message)
            .where(Message.sender_id == user.id)
            .order_by(Message.sent_at.desc())
            .limit(50)
        ).all()
        
        if not messages:
            response = "📭 Нет сообщений в истории"
        else:
            history = []
            for msg in messages:
                time = msg.sent_at.strftime("%d.%m %H:%M")
                text = msg.text if len(msg.text) < 100 else msg.text[:97] + "..."
                history.append(f"⏱️ <b>{time}</b>\n{text}")
            
            username = user.username or f"{user.first_name} {user.last_name or ''}".strip()
            response = (
                f"📜 История <b>{username}</b> (ID: {user.telegram_id}):\n\n" +
                "\n\n".join(history)
            )
        
        await message.answer(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /re_chat: {str(e)}")
        await message.answer("⚠️ Произошла ошибка при получении истории сообщений.")