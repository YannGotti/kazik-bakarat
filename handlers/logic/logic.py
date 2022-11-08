import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from states.userSettings import UserSetting
from keyboards.inline.admin import *

from services.service import *

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Защита от спама, подождите 25 сек")

@dp.callback_query_handler(gameData.filter(action="play"), state=None)
async def play_game(call: types.CallbackQuery, state: FSMContext):

    await call.message.edit_text(await select_updated_data(), reply_markup = await getBetsKeyboard())



    await UserSetting.IsGaming.set()

@dp.callback_query_handler(gameData.filter(action="red"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    print("Asd")
    await call.message.answer("Красное")
    await call.answer()

@dp.callback_query_handler(gameData.filter(action="cancel"), state=UserSetting.IsGaming)
async def red_bet(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вы вышли из игры", reply_markup = await getPlayKeyboard())
    await state.finish()
    

async def select_updated_data():
    return "Asd"