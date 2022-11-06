from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

gameData = CallbackData("post", "message_id", "action")

async def getCancelKeyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена",
                                 callback_data=gameData.new(action="cancel", message_id=1))
        ],
    ])
