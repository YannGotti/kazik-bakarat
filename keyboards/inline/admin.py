from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

gameData = CallbackData("post", "message_id", "action")

async def getCancelKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Отмена', callback_data=gameData.new(action="cancel", message_id=1)))

async def getPlayKeyboard():
    return InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton('Играть', callback_data=gameData.new(action="play", message_id=1)))

async def getBetsKeyboard():
    cancel = InlineKeyboardButton('Выйти', callback_data=gameData.new(action="cancel", message_id=1))
    redButton = InlineKeyboardButton('♦ Красное', callback_data=gameData.new(action="♦", message_id=1))
    greenButton = InlineKeyboardButton('❇ Ничья', callback_data=gameData.new(action="❇", message_id=1))
    blueButton = InlineKeyboardButton('♣ Черное', callback_data=gameData.new(action="♣", message_id=1))
    return InlineKeyboardMarkup(row_width=2).row(redButton, greenButton, blueButton, cancel)

async def getBetsValuesKeyboard():
    buttons = [
        [
            InlineKeyboardButton('1️⃣0️⃣0️⃣', callback_data=gameData.new(action="100", message_id=1)),
            InlineKeyboardButton('1️⃣0️⃣0️⃣0️⃣', callback_data=gameData.new(action="1000", message_id=1)),
            InlineKeyboardButton('1️⃣0️⃣0️⃣0️⃣0️⃣', callback_data=gameData.new(action="10000", message_id=1))
        ],
        [InlineKeyboardButton('ALL-IN - Все', callback_data=gameData.new(action="ALL", message_id=1))],
        [InlineKeyboardButton('Своя ставка', callback_data=gameData.new(action="custom", message_id=1))],
        [InlineKeyboardButton('Назад', callback_data=gameData.new(action="back", message_id=1))]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)