from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Мои данные"), KeyboardButton(text="Окак")]
        ],
        resize_keyboard=True
    )
    return keyboard
