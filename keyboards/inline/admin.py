from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

gameData = CallbackData("post", "message_id", "action")

async def getCancelKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Отмена', callback_data=gameData.new(action="cancel", message_id=1)))

async def getPlayKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Играть', callback_data=gameData.new(action="play", message_id=2)))

async def getBetsKeyboard():
    cancel = InlineKeyboardButton('Отмена', callback_data=gameData.new(action="cancel", message_id=1))
    redButton = InlineKeyboardButton('♦ Красное', callback_data=gameData.new(action="red", message_id=3))
    greenButton = InlineKeyboardButton('💹 Зеленое', callback_data=gameData.new(action="green", message_id=4))
    blueButton = InlineKeyboardButton('♣ Синее', callback_data=gameData.new(action="blue", message_id=5))
    return InlineKeyboardMarkup(row_width=2).row(redButton, greenButton, blueButton, cancel)