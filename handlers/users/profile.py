import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from services.service import userExists, addUser, getTwitchName, getMoneyUserString
from states.userSettings import UserSetting

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Защита от спама, подождите 25 сек")

@dp.message_handler(Text(equals=[SHOW_PROFILE, "/profile"]), state=None)
@dp.throttled(anti_flood, rate=0)
async def user_connect(message: types.Message):
    await message.delete()