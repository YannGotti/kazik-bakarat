import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from services.service import userExists, addUser, getTwitchName, getMoneyUserString
from states.userSettings import UserSetting


@dp.message_handler(Text(equals="aasd"), state=None)
async def asd(message: types.Message):
    await message.delete()
    await message.answer(getMoneyUserString(message.chat.id))