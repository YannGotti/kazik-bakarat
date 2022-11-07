import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from states.userSettings import UserSetting
from keyboards.inline.admin import *

from services.service import userExists, addUser, getTwitchName, getMoneyUserString

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Защита от спама, подождите 25 сек")

@dp.callback_query_handler(gameData.filter(action="play"), state=None)
async def play_game(call: types.CallbackQuery, state: FSMContext):
    await UserSetting.IsGaming.set()
    await call.message.edit_text("Иasdasd")

@dp.message_handler(state=UserSetting.IsGaming)
async def game_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer("asd")
    await state.finish