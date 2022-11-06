from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from messages import *

async def getUserKeyboard():
    keyboard = [[KeyboardButton(text=RESET_NICKNAME)]]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
