from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from services.service import *

adminData = CallbackData("post", "message_id", "action")



async def getAdminPanelButtons():

    if not isBetStarted():
        startStopGame = InlineKeyboardButton('Открыть ставки', callback_data=adminData.new(action="startGame", message_id=1))
    else:
        startStopGame = InlineKeyboardButton('Закрыть ставки', callback_data=adminData.new(action="stopGame", message_id=1))

    buttons = [
        [
            InlineKeyboardButton('♦', callback_data=adminData.new(action="♦", message_id=1)),
            InlineKeyboardButton('❇', callback_data=adminData.new(action="❇", message_id=1)),
            InlineKeyboardButton('♣', callback_data=adminData.new(action="♣", message_id=1))
        ],
        [
            startStopGame
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)