import os

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *

from keyboards.default.user import getUserKeyboard

from services.service import userExists, addUser, getTwitchName, getMoneyUserString
from states.userSettings import UserSetting

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.answer("Защита от спама, подождите 25 сек")


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=25)
async def start(message: types.Message):
    if (await bot.get_chat(message.chat.id)).type == "group":
        return

    if not userExists(message.from_user.id):
        addUser(message.from_user.id)

    twitch_name = getTwitchName(message.from_user.id)
    await message.answer("Здарова,заебал!\nhttps://t.me/muhanjanLotoSupport - По техническим вопросам и отслеживанием за обновлениями",
                         reply_markup=None if twitch_name is None else await getUserKeyboard())

    if twitch_name is None:
        await message.answer(ENTER_TWITCH_NICKNAME)
        await UserSetting.TwitchName.set()



    
