from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp

from messages import *

from services.service import addTwitchName, getTwitchName

from states.userSettings import UserSetting

from keyboards.default.user import getUserKeyboard
from keyboards.inline.admin import *


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Нельзя так часто")


@dp.message_handler(state=UserSetting.TwitchName)
async def add_twitch_name(message: types.Message, state: FSMContext):
    addTwitchName(message.chat.id, message.text)
    await message.answer(SET_NICKNAME + f"{getTwitchName(message.from_user.id)}", reply_markup=await getPlayKeyboard())
    await message.delete()
    await state.finish()

@dp.message_handler(Text(equals=[RESET_NICKNAME, "/change_twitch"]), state=None)
@dp.throttled(anti_flood, rate=0)
async def user_connect(message: types.Message):
    await message.delete()
    await message.answer(ENTER_TWITCH_NICKNAME, reply_markup=await getCancelKeyboard())
    await UserSetting.TwitchName.set()


@dp.callback_query_handler(gameData.filter(action="cancel"), state=UserSetting.TwitchName)
async def cancel_change_twitch(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Изменения отменены")
    await state.finish()