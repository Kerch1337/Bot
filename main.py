import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Загрузка переменных окружения
#load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки базы данных
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Проверка наличия обязательных переменных
required_vars = [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]
if None in required_vars:
    logger.error("Отсутствуют необходимые переменные окружения для БД!")
    exit(1)

# Создание подключения к БД
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель данных
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    full_name = Column(String)

# Создание таблиц
Base.metadata.create_all(bind=engine)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("Не найден BOT_TOKEN в переменных окружения!")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с кнопками
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Мои данные"), KeyboardButton(text="Окак")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    logger.info(f"Пользователь {message.from_user.full_name} начал общение")
    user = message.from_user
    await message.answer(
        "Привет, "+ user.first_name +"! Я просто бот. Можешь написать что-нибудь или выбрать команду:",
        reply_markup=get_main_keyboard()
    )

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text.lower()
    logger.info(f"Пользователь написал: {user_text}")

    if user_text.lower() == "привет":
        await message.answer("И тебе привет! 😊")
    elif user_text.lower() == "помощь":
        await message.answer("Вот доступные команды:\n/start - начать заново")
    elif user_text.lower() == "мои данные":
        user = message.from_user
        await message.answer(
            f"Ваши данные:\n"
            f"ID: {user.id}\n"
            f"Имя: {user.first_name}\n"
            f"Фамилия: {user.last_name or 'нет'}\n"
            f"Username: @{user.username}"
        )
    elif user_text.lower() == "окак":
        try:
            # Путь к изображению относительно текущего файла
            image_path = Path(__file__).parent / "images" / "okak.jpg"
        
            # Проверяем существование файла
            if not image_path.exists():
                raise FileNotFoundError(f"Файл {image_path} не найден")
        
            # Создаем объект файла
            photo = FSInputFile(image_path)
        
            await message.answer_photo(
                photo,
                caption="окак"
            )
        except Exception as e:
            logger.error(f"Ошибка отправки изображения: {e}")
            await message.answer("Не удалось загрузить изображение 😢")
    else:
        await message.answer(user_text[::-1])

if __name__ == "__main__":
    logger.info("Бот запущен и ожидает сообщений...")
    dp.run_polling(bot)