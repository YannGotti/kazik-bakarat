from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

gameData = CallbackData("post", "message_id", "action")

async def getCancelKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Отмена', callback_data=gameData.new(action="cancel", message_id=1)))

async def getPlayKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Играть', callback_data=gameData.new(action="play", message_id=2)))