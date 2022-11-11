import os

import typing

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from states.userSettings import UserSetting
from keyboards.inline.admin import *

from services.service import *

async def anti_flood_callback(*args, **kwargs):
    call = args[0]
    chat_id = call.message.chat.id
    await call.message.edit_text(ANTI_FLOOD)
    await call.answer()

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)


@dp.message_handler(commands=['shop'], state=None)
@dp.throttled(anti_flood, rate=1)
async def shop_open(message: types.Message):
    await message.delete()

    if not userExists(message.chat.id):
        await message.answer(NOT_REGISTER)
        return

    await message.answer(IN_GAME, reply_markup=await getPlayKeyboard())